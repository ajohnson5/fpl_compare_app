from random import randint
import random
import requests


# List of player ID's
squad_list_1 = [17, 313, 90, 96, 129, 137, 146, 402, 221, 331, 464, 18, 80, 309, 123]
squad_list_2 = [116, 157, 182, 194, 216, 224, 248, 137, 337, 237, 327, 142, 48, 27, 113]

# Dictionary replicating fpl api endpoint manager gameweek picks
squad_dict = {
    "active_chip": "bboost",
    "automatic_subs": [
        {
            "entry": 123,
            "element_in": 17,
            "element_out": 123,
            "event": 4,
        },
        {
            "entry": 123,
            "element_in": 129,
            "element_out": 313,
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
            "element": 402,
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
            "element": 18,
            "position": 12,
            "is_captain": False,
            "multiplier": 0,
        },
        {
            "element": 80,
            "position": 13,
            "is_captain": False,
            "multiplier": 0,
        },
        {
            "element": 309,
            "position": 14,
            "is_captain": False,
            "multiplier": 0,
        },
        {
            "element": 123,
            "position": 15,
            "is_captain": False,
            "multiplier": 0,
        },
    ],
}


squad_dict_2 = {
    "active_chip": "",
    "automatic_subs": [
        {
            "entry": 1223,
            "element_in": 116,
            "element_out": 113,
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
            "element": 142,
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
            "element": 113,
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
        potential_transfers_out = [x for x in range(1, 400) if x not in squad_list]

        for gameweek in TransferMock.gameweeks:
            num_transfers = randint(0, 11)

            transfers_in = random.sample(squad_list, num_transfers)

            transfers_out = random.sample(potential_transfers_out, num_transfers)

            for id_in, id_out in zip(transfers_in, transfers_out):
                transfers_made.append(self.make_mock_transfer(id_in, id_out, gameweek))

        return transfers_made


# Transfer pick mock data for managers over the whole season
transfers_1 = TransferMock(squad_list_1).transfers
transfers_2 = TransferMock(squad_list_2).transfers


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
