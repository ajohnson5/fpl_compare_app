import requests
from player import Player
from squad import Squad
import pandas as pd
import asyncio
import gcsfs

# df = pd.read_csv("players_raw.csv")
df = pd.read_parquet("gs://fpl_dev_bucket/2022/player_gameweek/")
df.set_index(["gameweek", "id"], inplace=True)


def manager_gw_picks_api(gw: int, manager_id):
    """Returns a list of dictionaries of all picks a manager made in a gameweek"""
    # Check for valid ID
    if (manager_id is None) or (not manager_id.isdigit()):
        return None

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

    return Squad(int(manager_id), squad_list, chip, stats)


def get_mini_league_managers(league_id: str):
    page = 1
    managers = {}
    url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/?page_standings={str(page)}"
    req = requests.get(url).json()

    check = True

    while check:
        check = req["standings"]["has_next"]
        for manager in req["standings"]["results"]:
            managers[manager["entry"]] = manager["entry_name"]

        if check and page < 5:
            page += 1
            print(page)
            url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/?page_standings={str(page)}"
            req = requests.get(url).json()
        else:
            return managers

    return managers
