from typing import Self

from player import Player
from nicegui import ui


class Squad:
    team_rotate = {"home": "", "away": "rotate-180 lg:rotate-0"}

    def __init__(self, manager_id: int, squad_list: list[Player], chip, stats: dict):
        self.manager_id = manager_id
        self.start_xi = squad_list[:11]
        self.bench = sorted(squad_list[11:], key=lambda x: x.actual_position)
        self.goalies = squad_list[0]
        self.defenders = [x for x in self.start_xi if x.actual_position == 2]
        self.midfielders = [x for x in self.start_xi if x.actual_position == 3]
        self.strikers = [x for x in self.start_xi if x.actual_position == 4]
        self.chip = chip
        self.stats = stats

    def players_by_position(self, position: int):
        if position == 1:
            return self.goalies
        elif position == 2:
            return self.defenders
        elif position == 3:
            return self.midfielders
        else:
            return self.strikers

    def compare_squad(self, squad_2: Self):
        # Compares two squads and puts common players
        # at the start of the lists for all positions
        self.layout = [
            self.bench,
            [self.goalies],
        ]
        squad_2.layout = [
            squad_2.bench,
            [squad_2.goalies],
        ]

        for position in [2, 3, 4]:
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

    def create_team_display(self, home):
        for position in self.layout[1:]:
            with ui.element("div").classes(
                "row-span-1 flex flex-row justify-around content-center "
                + Squad.team_rotate[home]
            ):
                for player in position:
                    player.create_card(home)

    def create_bench_display(self, home):
        with ui.row().classes(
            "flex flex-row w-full h-full justify-around content-center gap-x-0 pb-1"
        ):
            for player in self.layout[0]:
                player.create_card(home)
