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
app = firebase_admin.initialize_app()
db = firestore.client()


db_async = firestore_async.client()


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
    players = get_players(context.partition_key)

    load_players_batch(players, db)

    return None


#####################################################################
#####################################################################
##################### Temporary functions ###########################
#####################################################################
#####################################################################


def generate_gw_live_data():
    endpoint = {
        "elements": [],
        "explain": [],
    }
    for i in range(1, 606):
        endpoint["elements"].append(
            {
                "id": i,
                "stats": {
                    "minutes": random.randint(0, 90),
                    "total_points": random.randint(-3, 15),
                    "bonus": random.randint(0, 3),
                },
            }
        )

    return endpoint


mock_data = generate_gw_live_data()


def get_players(gw):
    gameweeks = get_gameweeks(gw)

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
            "gameweeks": gameweeks[str(player["id"])],
        }
    return players


def get_gameweeks(gw):
    req = mock_data

    gameweeks = {}
    for player in req["elements"]:
        gameweeks[str(player["id"])] = {
            f"gameweek_{gw}": {
                "minutes": player["stats"]["minutes"],
                "points": player["stats"]["total_points"],
                "bonus": player["stats"]["bonus"],
            }
        }

    return gameweeks


#####################################################################
#####################################################################
######################## Actual functions ###########################
#####################################################################
#####################################################################


# def get_gameweeks(gw):
#     url = f"https://fantasy.premierleague.com/api/event/{gw}/live/"
#     req = requests.get(url).json()

#     gameweeks = {
#     }
#     for player in req["elements"]:
#         gameweeks[player["id"]] = {
#             f"gameweek_{gw}":{
#             "minutes":player["stats"]["minutes"],
#             "points":player["stats"]["total_points"],
#             "bonus":player["stats"]["bonus"],
#         }
#     }


# def get_players(gw):

#     gameweeks = get_gameweeks(gw)

#     url = "https://fantasy.premierleague.com/api/bootstrap-static/"
#     req = requests.get(url).json()

#     players = {}
#     for player in req["elements"]:
#         players[str(player["id"])] = {
#             "first_name":player["first_name"],
#             "second_name":player["second_name"],
#             "web_name":player["web_name"],
#             "team_name":teams[player["team"]],
#             "total_points":player["total_points"],
#             "actual_position":player["element_type"],
#             "gameweeks":gameweeks[str(player["id"])]
#         }
#     return players
