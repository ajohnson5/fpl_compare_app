import requests
import pandas as pd
import aiohttp
import asyncio
import gcsfs

from player import Player
from squad import Squad

df_raw = pd.read_parquet(
    "gs://fpl_dev_bucket1/2022_player_gameweek_player_gameweek_38.parquet"
)

df = df_raw[
    [
        "first_name",
        "second_name",
        "position",
        "total_points",
        "team_name",
        "gameweek",
        "id",
    ]
]


df.set_index(["gameweek", "id"], inplace=True)


def manager_name(manager_id: int):
    url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/"
    req = requests.get(url).json()

    try:
        return req["name"]
    except KeyError:
        return


example_picks = {}


squad_dict = {
    "active_chip": "wildcard",
    "automatic_subs": [
        {
            "entry": 123,
            "element_in": 586,
            "element_out": 332,
            "event": 4,
        },
        {
            "entry": 123,
            "element_in": 81,
            "element_out": 254,
            "event": 7,
        },
    ],
    "entry_history": {"rank": 1},
    "picks": [
        {
            "element": 81,
            "position": 1,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 586,
            "position": 2,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 285,
            "position": 3,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 357,
            "position": 4,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 124,
            "position": 5,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 283,
            "position": 6,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 333,
            "position": 7,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 335,
            "position": 8,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 116,
            "position": 9,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 319,
            "position": 10,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 427,
            "position": 11,
            "is_captain": True,
            "multiplier": 2,
        },
        {
            "element": 254,
            "position": 12,
            "is_captain": False,
            "multiplier": 0,
        },
        {
            "element": 332,
            "position": 13,
            "is_captain": False,
            "multiplier": 0,
        },
        {
            "element": 85,
            "position": 14,
            "is_captain": False,
            "multiplier": 0,
        },
        {
            "element": 237,
            "position": 15,
            "is_captain": False,
            "multiplier": 0,
        },
    ],
}


squad_dict_2 = {
    "active_chip": "wildcard",
    "automatic_subs": [
        {
            "entry": 123,
            "element_in": 586,
            "element_out": 332,
            "event": 4,
        },
        {
            "entry": 123,
            "element_in": 81,
            "element_out": 254,
            "event": 7,
        },
    ],
    "entry_history": {"rank": 11},
    "picks": [
        {
            "element": 81,
            "position": 1,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 586,
            "position": 2,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 285,
            "position": 3,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 357,
            "position": 4,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 124,
            "position": 5,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 283,
            "position": 6,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 333,
            "position": 7,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 335,
            "position": 8,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 116,
            "position": 9,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 319,
            "position": 10,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 427,
            "position": 11,
            "is_captain": True,
            "multiplier": 2,
        },
        {
            "element": 254,
            "position": 12,
            "is_captain": False,
            "multiplier": 0,
        },
        {
            "element": 332,
            "position": 13,
            "is_captain": False,
            "multiplier": 0,
        },
        {
            "element": 85,
            "position": 14,
            "is_captain": False,
            "multiplier": 0,
        },
        {
            "element": 237,
            "position": 15,
            "is_captain": False,
            "multiplier": 0,
        },
    ],
}


def manager_gw_picks_api_temp(gw: int, manager_id: int):
    """Returns a list of dictionaries of all picks a manager made in a gameweek"""
    # Check for valid ID

    squad_list = []

    subs_in = {x["element_in"] for x in squad_dict["automatic_subs"]}
    subs_out = {x["element_out"] for x in squad_dict["automatic_subs"]}

    for pick in squad_dict["picks"]:
        id = pick["element"]
        player_series = df.loc[gw, id]
        if id in subs_in or id in subs_out:
            sub = True
        else:
            sub = False

        squad_list.append(
            Player(
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
            )
        )

    # stats["team_name"] = manager_name(manager_id)

    return Squad(
        manager_id=manager_id,
        squad_list=squad_list,
        chip=squad_dict["active_chip"],
        stats=squad_dict["entry_history"],
    )


def manager_gw_picks_api(gw: int, manager_id: int):
    """Returns a list of dictionaries of all picks a manager made in a gameweek"""
    # Check for valid ID

    url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/event/{gw}/picks/"
    req = requests.get(url).json()

    # Check if ID exists
    if "detail" in req:
        return None

    squad_list = []

    for pick in req["picks"]:
        player_series = df.loc[gw, pick["element"]]
        squad_list.append(
            Player(
                id=pick["element"],
                name=player_series["second_name"],
                first_name=player_series["first_name"],
                position=pick["position"],
                actual_position=player_series["position"],
                points=player_series["total_points"],
                team_name=player_series["team_name"],
                is_captain=pick["is_captain"],
                multiplier=pick["multiplier"],
            )
        )

    chip = req["active_chip"]

    stats = req["entry_history"]
    stats["team_name"] = manager_name(manager_id)

    return Squad(manager_id, squad_list, chip, stats)


def get_mini_league_managers_sync(league_id: int, page_num: int = 50):
    page = 1
    managers = {}
    url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/?page_standings={page}"
    req = requests.get(url).json()

    if not mini_league_check(req):
        return managers

    for manager in req["standings"]["results"]:
        managers[manager["entry"]] = manager["entry_name"]

    while req["standings"]["has_next"] and page <= page_num:
        page += 1
        url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/?page_standings={page}"
        req = requests.get(url).json()
        for manager in req["standings"]["results"]:
            managers[manager["entry"]] = manager["entry_name"]

    return managers


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


async def get_mini_league_managers(league_id: int, page_num: int = 100):
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


# if __name__ == "__main__":
#     # squad_1 = manager_gw_picks_api_temp(38, 13231)
#     # squad_2 = manager_gw_picks_api_temp(38, 1310)

#     # team_1, team_2 = squad_1.compare_squad(squad_2)

#     # for postition in team_1:
#     #     for player in postition:
#     #         print(player.position)
#     #         print(player.auto_sub)
#     #         print(player.starting)
#     #         print("####")

#     print(df.memory_usage(deep=True, index=True).sum())

#     print(df.dtypes)
