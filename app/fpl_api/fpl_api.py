import requests
import pandas as pd
import aiohttp
import asyncio
import gcsfs

from .player import PlayerGameweek
from .squad import SquadGameweek

col_list = [
    "first_name",
    "second_name",
    "position",
    "total_points",
    "team_name",
    "gameweek",
    "id",
]

df = pd.read_parquet(
    "gs://fpl_dev_bucket1/2022_player_gameweek_player_gameweek_38.parquet",
    columns=col_list,
)

df.set_index(["gameweek", "id"], inplace=True)


def get_manager_name(manager_id: int):
    url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/"
    req = requests.get(url).json()

    try:
        return req["name"]
    except KeyError:
        return


def get_manager_gw_transfers(
    gw: int,
    manager_id,
):
    url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/transfers/"
    req = requests.get(url).json()
    transfer_made = []
    if not req:
        return

    for transfer in reversed(req):
        if transfer["event"] == gw:
            transfer_made.append(transfer)
        elif transfer["event"] > gw:
            return transfer_made

    return transfer_made


def get_manager_gw_picks(
    gw: int, manager_id: int, manager_name: str, squad_dict_, transfers_list
):
    """Returns a list of dictionaries of all picks a manager made in a gameweek"""
    # Check for valid ID

    transfers_in, transfers_out = get_manager_gw_transfers(
        gw, manager_id, transfers_list
    )

    squad_list = []
    transfers_out_list = []

    subs_in = {x["element_in"] for x in squad_dict_["automatic_subs"]}
    subs_out = {x["element_out"] for x in squad_dict_["automatic_subs"]}

    for pick in squad_dict_["picks"]:
        id = pick["element"]
        player_series = df.loc[gw, id]
        if id in transfers_in:
            transfer_num = transfers_in.index(id)
        else:
            transfer_num = -1

        if id in subs_in or id in subs_out:
            sub = True
        else:
            sub = False

        squad_list.append(
            PlayerGameweek(
                id=id,
                name=player_series["second_name"],
                first_name=player_series["first_name"],
                position=pick["position"],
                actual_position=player_series["position"],
                points=player_series["total_points"],
                team_name=player_series["team_name"],
                is_captain=pick["is_captain"],
                multiplier=pick["multiplier"],
                auto_sub=sub,
                transfer=transfer_num,
            )
        )

    for pick in transfers_out:
        id = pick
        player_series = df.loc[gw, id]
        transfers_out_list.append(
            PlayerGameweek(
                id=id,
                name=player_series["second_name"],
                first_name=player_series["first_name"],
                position=16,
                actual_position=player_series["position"],
                points=player_series["total_points"],
                team_name=player_series["team_name"],
                is_captain=False,
                multiplier=0,
                auto_sub=False,
                transfer=-1,
            )
        )

    return SquadGameweek(
        manager_id=manager_id,
        manager_name=manager_name,
        squad_list=squad_list,
        chip=squad_dict_["active_chip"],
        stats=squad_dict_["entry_history"],
        transfers_out=transfers_out_list,
    )


async def get_mini_league_managers_async(session, league_id: int, page_num: int):
    page = 1
    managers = {}

    async with session:
        url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/?page_standings={page}"
        async with session.get(url) as resp:
            req = await resp.json()

        for manager in req["standings"]["results"]:
            managers[manager["entry"]] = manager["entry_name"]

        while req["standings"]["has_next"] and page <= page_num:
            page += 1
            url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/?page_standings={page}"
            async with session.get(url) as resp:
                req = await resp.json()
                for manager in req["standings"]["results"]:
                    managers[manager["entry"]] = manager["entry_name"]

    return managers


async def get_request(session, url):
    async with session.get(url) as resp:
        try:
            req = await resp.json(encoding="utf-8")
            return req["standings"]["results"]
        except aiohttp.client_exceptions.ContentTypeError:
            # Catch error message below
            # aiohttp.client_exceptions.ContentTypeError: 0,
            # message='Attempt to decode JSON with unexpected mimetype: text/html'
            return {}


async def get_large_mini_league_managers_async(session, league_id: int, page_num: int):
    async with session:
        managers = {}
        tasks = []
        for page in range(1, page_num + 1):
            url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/?page_standings={page}"
            tasks.append(asyncio.ensure_future(get_request(session, url)))

        manager_tasks = await asyncio.gather(*tasks)
        for page_ in manager_tasks:
            for manager in page_:
                managers[manager["entry"]] = manager["entry_name"]

    return managers


def mini_league_check(mini_league_json: dict):
    if "detail" in mini_league_json:
        return False
    else:
        return True


def mini_league_end_check(mini_league_json: dict):
    if mini_league_json["standings"]["results"] == []:
        return False
    else:
        return True


async def get_league_managers(league_id: int, page_num: int = 100):
    page = 1
    managers = {}
    connector = aiohttp.TCPConnector(limit=60)

    async with aiohttp.ClientSession(connector=connector) as session:
        url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/?page_standings={page}"
        async with session.get(url) as resp:
            req = await resp.json()

        if not mini_league_check(req):
            return managers

        end_url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/?page_standings={page_num}"
        async with session.get(end_url) as resp:
            req = await resp.json()

            if not mini_league_end_check(req):
                return await get_mini_league_managers_async(
                    session, league_id, page_num
                )
            else:
                return await get_large_mini_league_managers_async(
                    session, league_id, page_num
                )
