from random import randint
import random

import requests

# transfers = [
#     {
#         "element_in": 17,
#         "element_in_cost": 49,
#         "element_out": 28,
#         "element_out_cost": 53,
#         "event": 1,
#     },
#     {
#         "element_in": 90,
#         "element_in_cost": 50,
#         "element_out": 235,
#         "element_out_cost": 45,
#         "event": 1,
#     },
#     {
#         "element_in": 170,
#         "element_in_cost": 50,
#         "element_out": 257,
#         "element_out_cost": 45,
#         "event": 1,
#     },
#     {
#         "element_in": 221,
#         "element_in_cost": 50,
#         "element_out": 64,
#         "element_out_cost": 45,
#         "event": 1,
#     },
#     {
#         "element_in": 593,
#         "element_in_cost": 50,
#         "element_out": 98,
#         "element_out_cost": 45,
#         "event": 1,
#     },

# ]


# transfers_2 =  [
#     {
#         "element_in": 337,
#         "element_in_cost": 50,
#         "element_out": 189,
#         "element_out_cost": 45,
#         "event": 1,
#     },
#     {
#         "element_in": 327,
#         "element_in_cost": 50,
#         "element_out": 12,
#         "element_out_cost": 45,
#         "event": 1,
#     },
#     {
#         "element_in": 157,
#         "element_in_cost": 68,
#         "element_out": 352,
#         "element_out_cost": 70,
#         "event": 2,
#     },
# ]


# List of player ID's
squad_list_1 = [17, 313, 90, 96, 129, 137, 146, 170, 221, 331, 464, 546, 512, 499, 593]
squad_list_2 = [116, 157, 182, 194, 216, 224, 248, 137, 337, 237, 327, 546, 48, 27, 523]

# Dictionary replicating fpl api endpoint manager gameweek picks
squad_dict = {
    "active_chip": "wildcard",
    "automatic_subs": [
        {
            "entry": 123,
            "element_in": 17,
            "element_out": 546,
            "event": 4,
        },
        {
            "entry": 123,
            "element_in": 129,
            "element_out": 512,
            "event": 7,
        },
    ],
    "entry_history": {"rank": 1, "points": 65},
    "picks": [
        {
            "element": 17,
            "position": 1,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 313,
            "position": 2,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 90,
            "position": 3,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 96,
            "position": 4,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 129,
            "position": 5,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 137,
            "position": 6,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 146,
            "position": 7,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 170,
            "position": 8,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 221,
            "position": 9,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 331,
            "position": 10,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 464,
            "position": 11,
            "is_captain": True,
            "multiplier": 3,
        },
        {
            "element": 546,
            "position": 12,
            "is_captain": False,
            "multiplier": 0,
        },
        {
            "element": 512,
            "position": 13,
            "is_captain": False,
            "multiplier": 0,
        },
        {
            "element": 499,
            "position": 14,
            "is_captain": False,
            "multiplier": 0,
        },
        {
            "element": 593,
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
            "entry": 1223,
            "element_in": 116,
            "element_out": 546,
            "event": 4,
        },
        {
            "entry": 1234,
            "element_in": 137,
            "element_out": 27,
            "event": 7,
        },
    ],
    "entry_history": {"rank": 11, "points": 41},
    "picks": [
        {
            "element": 116,
            "position": 1,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 157,
            "position": 2,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 182,
            "position": 3,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 194,
            "position": 4,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 216,
            "position": 5,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 224,
            "position": 6,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 248,
            "position": 7,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 137,
            "position": 8,
            "is_captain": True,
            "multiplier": 2,
        },
        {
            "element": 337,
            "position": 9,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 237,
            "position": 10,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 327,
            "position": 11,
            "is_captain": False,
            "multiplier": 1,
        },
        {
            "element": 546,
            "position": 12,
            "is_captain": False,
            "multiplier": 0,
        },
        {
            "element": 48,
            "position": 13,
            "is_captain": False,
            "multiplier": 0,
        },
        {
            "element": 27,
            "position": 14,
            "is_captain": False,
            "multiplier": 0,
        },
        {
            "element": 523,
            "position": 15,
            "is_captain": False,
            "multiplier": 0,
        },
    ],
}


class TransferMock:
    gameweeks = range(1, 39)

    def __init__(self, squad_list: list):
        self.transfers = self.make_mock_data(squad_list)

    def make_mock_transfer(self, id_in: int, id_out: int, gameweek: int) -> dict:
        return {
            "element_in": id_in,
            "element_in_cost": randint(40, 140),
            "element_out": id_out,
            "element_out_cost": randint(40, 140),
            "event": gameweek,
        }

    def make_mock_data(self, squad_list: list):
        transfers_made = []
        potential_transfers_out = [x for x in range(1, 605) if x not in squad_list]

        for gameweek in TransferMock.gameweeks:
            num_transfers = randint(0, 6)

            transfers_in = random.sample(squad_list, num_transfers)

            transfers_out = random.sample(potential_transfers_out, num_transfers)

            for id_in, id_out in zip(transfers_in, transfers_out):
                transfers_made.append(self.make_mock_transfer(id_in, id_out, gameweek))

        return transfers_made


formations = {
    "352": [1, 3, 5, 2],
    "343": [1, 3, 4, 3],
    "451": [1, 4, 5, 1],
    "442": [1, 4, 4, 2],
    "433": [1, 4, 3, 3],
    "541": [1, 5, 4, 1],
    "532": [1, 5, 3, 2],
    "523": [1, 5, 2, 3],
}


def get_players_generator():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    req = requests.get(url).json()

    players = {}

    goalies = []
    defenders = []
    midfielders = []
    strikers = []
    for player in req["elements"]:
        id = player["id"]
        players[id] = {
            "first_name": player["first_name"],
            "second_name": player["second_name"],
            "web_name": player["web_name"],
            "total_points": player["total_points"],
            "team": player["team"],
            "element_type": player["element_type"],
            "minutes": player["minutes"],
            "now_cost": player["now_cost"],
        }

        if player["element_type"] == 1:
            goalies.append(player["id"])
        if player["element_type"] == 2:
            defenders.append(player["id"])
        if player["element_type"] == 3:
            midfielders.append(player["id"])
        if player["element_type"] == 4:
            strikers.append(player["id"])

    return players, [goalies, defenders, midfielders, strikers]


class RandomSquadGenerator:
    max_player_position_count = [2, 5, 5, 3]

    formations = [
        [1, 3, 5, 2],
        [1, 3, 4, 3],
        [1, 4, 5, 1],
        [1, 4, 4, 2],
        [1, 4, 3, 3],
        [1, 5, 4, 1],
        [1, 5, 3, 2],
        [1, 5, 2, 3],
    ]

    players, player_positions = get_players_generator()

    def __init__(
        self,
    ):
        self.formation = self.get_formation()

    def get_formation(
        self,
    ):
        return random.choice(RandomSquadGenerator.formations)

    def random_squad_ids(
        self,
    ):
        self.squad_ids = []
        for i, position in enumerate(RandomSquadGenerator.max_player_position_count):
            self.squad_ids.append(
                (random.sample(RandomSquadGenerator.player_positions[i], position))
            )

    def check_player_teams(
        self,
    ):
        self.team_counter = {i: 0 for i in range(1, 21)}
        self.team_cost = 0
        for position in self.squad_ids:
            for player in position:
                self.team_cost += RandomSquadGenerator.players[player]["now_cost"]
                if self.team_cost > 1000:
                    return False
                if self.team_counter[RandomSquadGenerator.players[player]["team"]] < 3:
                    self.team_counter[RandomSquadGenerator.players[player]["team"]] += 1
                else:
                    return False

        return True

    def generate_squad(
        self,
    ):
        self.squad = []
        for position in self.squad_ids:
            for player in position:
                self.squad.append(RandomSquadGenerator.players[player])

    def create_random_squad(
        self,
    ):
        self.random_squad_ids()

        if self.check_player_teams():
            self.generate_squad()
        else:
            print("Retry")
            self.create_random_squad()


if __name__ == "__main__":
    generator = RandomSquadGenerator()

    generator.create_random_squad()

    print(generator.squad_ids)

    print(generator.squad)
    sum = 0
    for position in generator.squad_ids:
        for player in position:
            print(RandomSquadGenerator.players[player]["second_name"])
            sum += RandomSquadGenerator.players[player]["now_cost"]

    print(generator.team_counter)

    print(sum / 10)


# Transfer pick mock data for managers over the whole season
transfers_1 = TransferMock(squad_list_1).transfers

transfers_2 = TransferMock(squad_list_2).transfers
