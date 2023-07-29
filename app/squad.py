from typing import Self

from player import Player
from nicegui import ui


class Squad:
    team_rotate = {"home": "", "away": "rotate-180 lg:rotate-0"}

    def __init__(
        self,
        manager_id: int,
        manager_name: str,
        squad_list: list[Player],
        chip,
        stats: dict,
    ):
        self.manager_id = manager_id
        self.manager_name = manager_name
        self.start_xi = squad_list[:11]
        self.bench = sorted(squad_list[11:15], key=lambda x: x.actual_position)
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
            return [x for x in self.start_xi if x.actual_position == 2]
        elif position == 3:
            return [x for x in self.start_xi if x.actual_position == 3]
        else:
            return [x for x in self.start_xi if x.actual_position == 4]

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

    def create_manager_display(
        self,
    ):
        with ui.element("div").classes(
            "w-full h-[50px] flex flex-row content-center rounded-t-xl "
            "bg-slate-50/30"
        ):
            ui.label(self.manager_name).classes(
                "text-center w-full text-lg lg:text-2xl text-stone-100 font-medium"
            )

        with ui.element("div").classes(
            "w-full h-[100px]  flex flex-row content-center bg-slate-50/30 "
            "rounded-b-xl"
        ):
            ui.label(self.stats["points"]).classes(
                "text-center w-full text-stone-100 text-5xl md:text-7xl font-medium"
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
                    "col-span-1 flex flex-row justify-between"
                ):
                    ui.label("Transfers In").classes(
                        "w-1/2 text-center text-white text-2xl font-medium font-sans"
                    )
                    ui.label("Transfers Out").classes(
                        "w-1/2 text-center text-white text-2xl font-medium font-sans"
                    )
                for transfer in zip(self.transfers_in, self.transfers_out):
                    transfer[0].transfer_card(transfer[1], home)
            else:
                ui.label("No Transfers Made").classes(
                    "w-full text-center text-2xl font-medium text-white mt-2"
                )
