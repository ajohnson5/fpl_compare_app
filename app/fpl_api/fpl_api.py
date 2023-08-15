import requests
import aiohttp
import asyncio
import firebase_admin
from firebase_admin import firestore_async

from .player import PlayerGameweek
from .squad import SquadGameweek

firebase_admin.initialize_app()
db = firestore_async.client()


def get_manager_name(manager_id: int):
    """
    Returns the manager name for a given manager id - otherwise returns none
    """
    url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/"
    req = requests.get(url).json()

    try:
        return req["name"]
    except KeyError:
        return


def get_manager_gw_transfers(gw: int, manager_id):
    """
    Finds the transfers for a given manager on a specifed gameweek

    Returns two lists with the id's of the players transferred in
    and players transferred out
    """

    url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/transfers/"
    req = requests.get(url).json()

    transfers_in = {}
    transfers_out = []
    counter = 0
    for transfer in req:
        if transfer["event"] == gw:
            transfers_in[transfer["element_in"]] = {
                "element_in_cost": transfer["element_in_cost"],
                "element_out_cost": transfer["element_out_cost"],
                "transfer_order": counter,
            }
            transfers_out.append(
                {
                    "element": transfer["element_out"],
                    "position": 16 + counter,
                    "is_captain": False,
                    "is_vice_captain": False,
                    "multiplier": 0,
                }
            )
        elif transfer["event"] > gw:
            return transfers_in, transfers_out
        counter += 1

    return transfers_in, transfers_out


async def get_firestore_request(collection, pick_dict):
    """
    Retrieve player data from firestore and merge with current player dictionary
    """
    doc = await collection.document(str(pick_dict["element"])).get()
    return pick_dict | doc.to_dict()


async def get_manager_gw_picks(gw: int, manager_id: int, manager_name: str):
    """
    Returns a SquadGameweek object for a managers team in a gameweek
    """

    url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/event/{gw}/picks/"

    req = requests.get(url).json()

    if not req["picks"]:
        return

    squad_list = []
    # Get transfers in and transfers out for specified gameweek
    transfers_in, transfers_out = get_manager_gw_transfers(gw, manager_id)

    # Create sets of the ids for the players automatically subbed in and subbed out
    subs_in = {x["element_in"] for x in req["automatic_subs"]}
    subs_out = {x["element_out"] for x in req["automatic_subs"]}

    # Gather firestore request coroutines and concatenate firestore request to each
    # player pick dict
    tasks = []

    for pick in req["picks"] + transfers_out:
        collection = db.collection("players")
        tasks.append(asyncio.ensure_future(get_firestore_request(collection, pick)))

    # Iterate through picks and create Player objects
    # for pick in picks_complete:
    for coroutine in asyncio.as_completed(tasks):
        pick = await coroutine
        id = pick["element"]
        # If player id is in transfer in then set transfer var equal to the associated
        # transfer dict
        if id in transfers_in:
            transfer = transfers_in[id]
        else:
            transfer = None

        # If id in subs in or subs_out then set subs flag to True. Note if player
        # starting and in one of these two sets then it must be subbed in
        if id in subs_in or id in subs_out:
            sub = True
        else:
            sub = False

        squad_list.append(
            PlayerGameweek(
                id=id,
                second_name=pick["second_name"],
                first_name=pick["first_name"],
                web_name=pick["web_name"],
                squad_order=pick["position"],
                position=pick["actual_position"],
                points=pick["gameweeks"][f"gameweek_{gw}"]["points"],
                total_points=pick["total_points"],
                bonus_points=pick["gameweeks"][f"gameweek_{gw}"]["bonus"],
                minutes=pick["gameweeks"][f"gameweek_{gw}"]["minutes"],
                team_name=pick["team_name"],
                is_captain=pick["is_captain"],
                multiplier=pick["multiplier"],
                auto_sub=sub,
                transfer=transfer,
                cost=10,
            )
        )
    # Sort squadlist based on the squad order
    squad_list.sort(key=lambda x: x.squad_order)
    return SquadGameweek(
        manager_id=manager_id,
        manager_name=manager_name,
        squad_list=squad_list,
        chip=req["active_chip"],
        stats=req["entry_history"],
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
