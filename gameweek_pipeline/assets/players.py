from dagster import asset
import requests
import random
import asyncio
import firebase_admin
from firebase_admin import firestore_async
from firebase_admin import firestore


from gameweek_pipeline.partitions import gameweek_partitions_def


teams = {
    1: "Arsenal",
    2: "Aston Villa",
    3: "Bournemouth",
    4: "Brentford",
    5: "Brighton",
    6: "Burnley",
    7: "Chelsea",
    8: "Crystal Palace",
    9: "Everton",
    10: "Fulham",
    11: "Liverpool",
    12: "Luton",
    13: "Man City",
    14: "Man Utd",
    15: "Newcastle",
    16: "Nott'm Forest",
    17: "Sheffield Utd",
    18: "Spurs",
    19: "West Ham",
    20: "Wolves",
}


# Batch function takes ~8 seconds
def load_players_batch(data, db):
    batch = db.batch()
    counter = 0
    for key, value in data.items():
        player_ref = db.collection("players").document(key)
        batch.set(player_ref, value, merge=True)
        counter += 1
        if counter == 500:
            batch.commit()
            batch = db.batch()


# Sync function takees ~38 seconds for each partition
def load_players_sync(data, db):
    for key, value in data.items():
        db.collection("players").document(key).set(value, merge=True)


# Async function takees ~32 seconds for each partition
async def load_players_async(data, db):
    for key, value in data.items():
        await db.collection("players").document(key).set(value, merge=True)


#####################################################################
#####################################################################
############################## Asset ###############################
#####################################################################
#####################################################################


@asset(
    partitions_def=gameweek_partitions_def,
)
def players(context) -> None:
    firebase_admin.initialize_app()
    client = firestore.client()

    players = get_gameweeks(context.partition_key)

    load_players_batch(players, client)

    return None


#####################################################################
#####################################################################
######################## Actual functions ###########################
#####################################################################
#####################################################################


def get_gameweeks(gw):
    url = f"https://fantasy.premierleague.com/api/event/{gw}/live/"
    req = requests.get(url).json()

    players = get_players(gw)

    for player in req["elements"]:
        players[str(player["id"])]["gameweeks"] = {
            f"gameweek_{gw}": {
                "minutes": player["stats"]["minutes"],
                "points": player["stats"]["total_points"],
                "bonus": player["stats"]["bonus"],
            }
        }
    return players


def get_players(gw):
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    req = requests.get(url).json()

    players = {}
    for player in req["elements"]:
        players[str(player["id"])] = {
            "first_name": player["first_name"],
            "second_name": player["second_name"],
            "web_name": player["web_name"],
            "team_name": teams[player["team"]],
            "total_points": player["total_points"],
            "actual_position": player["element_type"],
        }
    return players
