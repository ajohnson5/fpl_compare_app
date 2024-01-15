from dagster import asset
import requests
from gameweek_pipeline.partitions import gameweek_partitions_def
from .fixtures import teams, teams_shorted


def get_players(gw: str) -> dict:
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    req = requests.get(url).json()

    players = {}

    try:
        for player in req["elements"]:
            players[str(player["id"])] = {
                "first_name": player["first_name"],
                "second_name": player["second_name"],
                "web_name": player["web_name"],
                "team_name": teams[player["team"]],
                "team_name_short": teams_shorted[player["team"]],
                "total_points": player["total_points"],
                "actual_position": player["element_type"],
            }
    except KeyError:
        raise ("elements key does not exist in the returned JSON. Site down.")

    return players


def get_gameweeks(gw: str) -> dict:
    url = f"https://fantasy.premierleague.com/api/event/{gw}/live/"
    req = requests.get(url).json()

    players = get_players(gw)

    try:
        for player in req["elements"]:
            players[str(player["id"])]["gameweeks"] = {
                f"gameweek_{gw}": {
                    "minutes": player["stats"]["minutes"],
                    "points": player["stats"]["total_points"],
                    "bonus": player["stats"]["bonus"],
                }
            }
    except KeyError:
        raise (
            f"elements key does not exist in the returned JSON. Gameweek {gw} "
            "exceeds bounds."
        )

    return players


@asset(
    partitions_def=gameweek_partitions_def, required_resource_keys={"firestore_client"}
)
def players(context) -> None:
    players = get_gameweeks(context.partition_key)

    context.resources.firestore_client.load_batch("players", players)

    return None
