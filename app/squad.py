from typing import Self

from player import Player, PlayerGameweek
from nicegui import ui
import requests
import random
from random import randint


class Squad:
    def __init__(self, squad_list, cost):
        self.layout = squad_list
        self.cost = cost

    def create_team_display(
        self,
    ):
        for position in self.layout:
            with ui.element("div").classes(
                "row-span-1 flex flex-row justify-around content-center h-full "
                "max-h-[100px]"
            ):
                for player in position:
                    player.create_card()

    def create_squad_summary_display(
        self,
    ):
        with ui.element("div").classes(
            "w-full h-[40px] flex flex-row content-center rounded-t-xl justify-center "
            "bg-slate-50/30 relative"
        ):
            ui.label("Squad Summary").classes(
                "text-center w-full text-lg lg:text-2xl text-stone-100 font-medium "
                "leading-none"
            )

        with ui.element("div").classes("w-full flex flex-row gap-x-0"):
            with ui.column().classes("grow flex flex-row gap-y-0"):
                ui.element("div").classes("h-1/2 w-full ").style(
                    "border-top: 10px solid rgb(248 250 252);border-left: 0px solid "
                    "transparent;border-right: 5px solid transparent; opacity:0.3;"
                )
                ui.element("div").classes("h-1/2 w-full ").style(
                    "border-bottom: 10px solid rgb(248 250 252);border-left: 0px solid "
                    "transparent;border-right: 5px solid transparent; opacity:0.3;"
                )

            ui.label("FPLCOMPARE").classes(
                "text-center w-auto font-medium rounded-full text-stone-100"
            )

            with ui.column().classes("grow flex flex-row gap-y-0"):
                ui.element("div").classes("h-1/2 w-full ").style(
                    "border-top: 10px solid rgb(248 250 252);border-left: 5px solid "
                    "transparent;border-right: 0px solid transparent; opacity:0.3;"
                )
                ui.element("div").classes("h-1/2 w-full ").style(
                    "border-bottom: 10px solid rgb(248 250 252);border-left: 5px solid "
                    "transparent;border-right: 0px solid transparent; opacity:0.3;"
                )

        with ui.element("div").classes(
            "w-full h-[100px] flex flex-row content-center bg-slate-50/30 rounded-b-xl"
        ):
            ui.label(f"£{self.cost/10}").classes(
                "text-center w-full text-stone-100 text-5xl md:text-7xl font-medium "
                "mt-1"
            )


class SquadGameweek:
    team_rotate = {"home": "", "away": "rotate-180 lg:rotate-0"}

    def __init__(
        self,
        manager_id: int,
        manager_name: str,
        squad_list: list[PlayerGameweek],
        chip,
        stats: dict,
    ):
        self.manager_id = manager_id
        self.manager_name = manager_name
        self.start_xi = squad_list[:11]
        self.bench = sorted(squad_list[11:15], key=lambda x: x.position)
        self.transfers_in = sorted(
            [player for player in squad_list if isinstance(player.transfer, dict)],
            key=lambda x: x.transfer["transfer_order"],
        )
        self.transfers_out = squad_list[15:]
        self.chip = chip
        self.stats = stats

    def players_by_position(self, position: int):
        if position == 1:
            return [self.start_xi[0]]
        elif position == 2:
            return [x for x in self.start_xi if x.position == 2]
        elif position == 3:
            return [x for x in self.start_xi if x.position == 3]
        else:
            return [x for x in self.start_xi if x.position == 4]

    def compare_squad(self, squad_2: Self):
        # Compares two squads and puts common players
        # at the start of the lists for all positions
        self.layout = []
        squad_2.layout = []

        for position in [1, 2, 3, 4]:
            if position == 1:
                self.layout.append(self.players_by_position(position))
                squad_2.layout.append(squad_2.players_by_position(position))
            else:
                squad_1_players_in_pos = self.players_by_position(position)
                squad_2_players_in_pos = squad_2.players_by_position(position)

                common_players = self.get_common_players_position(
                    squad_1_players_in_pos, squad_2_players_in_pos
                )

                self.layout.append(
                    sorted(
                        [y for y in squad_1_players_in_pos if y in common_players],
                        key=common_players.index,
                    )
                    + [x for x in squad_1_players_in_pos if x not in common_players]
                )
                squad_2.layout.append(
                    sorted(
                        [y for y in squad_2_players_in_pos if y in common_players],
                        key=common_players.index,
                    )
                    + [x for x in squad_2_players_in_pos if x not in common_players]
                )

    def get_common_players_position(self, squad_1_position, squad_2_position):
        return list(set(squad_1_position).intersection(squad_2_position))

    def create_manager_display(self, gameweek):
        with ui.element("div").classes(
            "w-full h-[40px] flex flex-row content-center rounded-t-xl justify-center "
            "bg-slate-50/30 relative"
        ):
            ui.label(self.manager_name).classes(
                "text-center w-full text-lg lg:text-2xl text-stone-100 font-medium "
                "leading-none"
            )

        with ui.element("div").classes("w-full flex flex-row gap-x-0"):
            with ui.column().classes("grow flex flex-row gap-y-0"):
                ui.element("div").classes("h-1/2 w-full ").style(
                    "border-top: 10px solid rgb(248 250 252);border-left: 0px solid "
                    "transparent;border-right: 5px solid transparent; opacity:0.3;"
                )
                ui.element("div").classes("h-1/2 w-full ").style(
                    "border-bottom: 10px solid rgb(248 250 252);border-left: 0px solid "
                    "transparent;border-right: 5px solid transparent; opacity:0.3;"
                )

            ui.label(f"Gameweek {gameweek}").classes(
                "text-center w-auto font-medium rounded-full text-stone-100"
            )

            with ui.column().classes("grow flex flex-row gap-y-0"):
                ui.element("div").classes("h-1/2 w-full ").style(
                    "border-top: 10px solid rgb(248 250 252);border-left: 5px solid "
                    "transparent;border-right: 0px solid transparent; opacity:0.3;"
                )
                ui.element("div").classes("h-1/2 w-full ").style(
                    "border-bottom: 10px solid rgb(248 250 252);border-left: 5px solid "
                    "transparent;border-right: 0px solid transparent; opacity:0.3;"
                )

        with ui.element("div").classes(
            "w-full h-full  flex flex-row content-center bg-slate-50/30 rounded-b-xl"
        ):
            ui.label(self.stats["points"]).classes(
                "text-center w-full text-stone-100 text-5xl md:text-7xl font-medium "
                "mt-1"
            )
            ui.label("Points").classes("text-center w-full text-stone-100")

    def create_team_display(self, home):
        for position in self.layout:
            with ui.element("div").classes(
                "row-span-1 flex flex-row justify-around content-center h-full "
                "max-h-[100px] " + Squad.team_rotate[home]
            ):
                for player in position:
                    player.create_card(home)

    def create_bench_display(self, home):
        with ui.element("div").classes(
            "flex flex-row w-full justify-around content-center gap-x-0"
        ).classes("player-card-height"):
            for player in self.bench:
                player.create_card(home)

    def create_transfer_display(self, home):
        with ui.element("div").classes("w-full"):
            if self.transfers_in:
                with ui.element("div").classes(
                    "col-span-1 flex flex-row justify-around"
                ):
                    ui.label("Transfers In").classes(
                        " text-center text-stone-100 text-2xl font-medium "
                        "font-sans grow"
                    )

                    ui.label().classes("w-[50px]")
                    ui.label("Transfers Out").classes(
                        " text-center text-stone-100 text-2xl font-medium "
                        "font-sans grow"
                    )
                for transfer in zip(self.transfers_in, self.transfers_out):
                    transfer[0].transfer_card(transfer[1], home)
            else:
                ui.label("No Transfers Made").classes(
                    "w-full text-center text-2xl font-medium text-stone-100 mt-2"
                )


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
        squad_list = []

        for position in self.squad_ids:
            position_list = []
            for player_id in position:
                player_dict = RandomSquadGenerator.players[player_id]
                position_list.append(
                    Player(
                        id=player_id,
                        second_name=player_dict["second_name"],
                        first_name=player_dict["first_name"],
                        web_name=player_dict["web_name"],
                        position=player_dict["element_type"],
                        team_name=player_dict["team"],
                        cost=player_dict["now_cost"],
                    )
                )
            squad_list.append(position_list)

        self.squad = Squad(squad_list, self.team_cost)

    def create_random_squad(
        self,
    ):
        self.random_squad_ids()

        if self.check_player_teams():
            self.generate_squad()
        else:
            print("Retry")
            self.create_random_squad()
