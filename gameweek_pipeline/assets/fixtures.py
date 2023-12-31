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

teams_shorted = {
    1: "ARS",
    2: "AVL",
    3: "BOU",
    4: "BRE",
    5: "BHA",
    6: "BUR",
    7: "CHE",
    8: "CRY",
    9: "EVE",
    10: "FUL",
    11: "LIV",
    12: "LUT",
    13: "MCI",
    14: "MUN",
    15: "NEW",
    16: "NFO",
    17: "SHU",
    18: "TOT",
    19: "WHU",
    20: "WOL",
}

teams_FDR = {
    1: 5,
    2: 3,
    3: 1,
    4: 3,
    5: 3,
    6: 1,
    7: 3,
    8: 2,
    9: 1,
    10: 2,
    11: 4,
    12: 1,
    13: 5,
    14: 4,
    15: 4,
    16: 2,
    17: 1,
    18: 4,
    19: 2,
    20: 2,
}

#####################################################################
#####################################################################
############################## Asset ################################
#####################################################################
#####################################################################


@asset(
    partitions_def=gameweek_partitions_def, required_resource_keys={"firestore_client"}
)
def fixtures(context) -> None:
    upcoming_fixtures = get_next_fixtures(context.partition_key)

    context.resources.firestore_client.load_batch("fixtures", upcoming_fixtures)

    return None


#####################################################################
#####################################################################
############################ Functions ##############################
#####################################################################
#####################################################################


def get_next_fixtures(gw):
    fixtures = {i: [] for i in range(1, 21)}

    for j in range(1, 11):
        url = f"https://fantasy.premierleague.com/api/fixtures/?event={int(gw)+j}"
        req = requests.get(url).json()

        for fixture in req:
            fixtures[fixture["team_h"]].append(
                {
                    "fixture": teams_shorted[fixture["team_a"]],
                    "FDR": teams_FDR[fixture["team_a"]],
                    "home": "H",
                }
            )
            fixtures[fixture["team_a"]].append(
                {
                    "fixture": teams_shorted[fixture["team_h"]],
                    "FDR": teams_FDR[fixture["team_h"]],
                    "home": "A",
                }
            )

    next_5_fixtures = {f"gameweek_{int(gw)+k}": {} for k in range(5)}
    for k in range(5):
        for key, value in fixtures.items():
            next_5_fixtures[f"gameweek_{int(gw)+k}"][teams[key]] = value[k : k + 5]

    return next_5_fixtures
