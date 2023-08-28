from dagster import asset
import requests
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

#####################################################################
#####################################################################
############################## Asset ################################
#####################################################################
#####################################################################


@asset(
    partitions_def=gameweek_partitions_def, required_resource_keys={"firestore_client"}
)
def players(context) -> None:
    players = get_gameweeks(context.partition_key)

    context.resources.firestore_client.load_batch("players", players)

    return None


#####################################################################
#####################################################################
############################ Functions ##############################
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
