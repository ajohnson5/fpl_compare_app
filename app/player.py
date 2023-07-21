from nicegui import ui

player_label = (
    "w-full h-1/2 text-center align-middle "
    "text-xs font-medium tracking-tighter leading-tight "
)
card_width = " w-[60px]"
# shirt_width = " w-[35px] sm:w-[40px] "
shirt_image_div = (
    "col-span-1 row-span-2 grid-cols-1 grid-rows-1 flex "
    "justify-center items-center relative"
)


class Player:
    team_color = {"home": "sky-500", "away": "red-500"}

    def __init__(
        self,
        id: int,
        name: str,
        first_name: str,
        position: int,
        actual_position: int,
        points: int,
        team_name: str,
        is_captain: bool,
        multiplier: int,
        auto_sub: bool,
        transfer: int,
    ):
        self.id = id
        self.name = name
        self.first_name = first_name
        self.position = position
        self.actual_position = actual_position
        self.starting = position <= 11
        self.points = points
        self.actual_points = points * multiplier if multiplier else points
        self.team_name = team_name
        self.is_captain = is_captain
        self.multiplier = multiplier
        self.auto_sub = auto_sub
        self.transfer = transfer

    def __eq__(self, other):
        if self.id == other.id:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.id, self.actual_position))

    def __bool__(self):
        return self.id is not None  # <--- added "return"

    def create_player_dialog(
        self,
    ):
        with ui.dialog() as dialog, ui.card().classes("relative w-72 h-48"):
            ui.label(f"{self.first_name} {self.name}").classes(
                "w-full text-center text-lg text-zinc-900 font-medium font-sans "
                "align-middle"
            )
            ui.separator()
            close_icon = ui.icon("close", size="32px").classes(
                "absolute top-2 right-2 text-zinc-900 hover:bg-zinc-300 rounded-full "
                "hover:cursor-pointer"
            )
            close_icon.on("click", dialog.close)

        return dialog

    def create_transfer_dialog(self, other_player):
        with ui.dialog() as dialog, ui.card().classes("relative w-72"):
            ui.label("Transfer").classes(
                "w-full text-center text-lg text-zinc-900 font-medium font-sans "
                "align-middle"
            )
            ui.separator()
            # Transfer point cost = 2 for 1st transfer and 0 otherwise (self.transfer)
            # evaluates to 0 apart from the first transfer
            ui.label(f"Transfer Point Cost: {(int(self.transfer <1))*2}")
            ui.label("Transfer Cost: ")
            ui.label("Transfer Revenue: ")
            ui.label(f"Point Profit: {self.actual_points - other_player.actual_points}")

            close_icon = ui.icon("close", size="32px").classes(
                "absolute top-2 right-2 text-zinc-900 hover:bg-zinc-300 "
                "hover:cursor-pointer rounded-full"
            )
            close_icon.on("click", dialog.close)

        return dialog

    def create_card(self, home, transfer=False):
        with ui.element("div").classes(
            "flex flex-row  flex-1 h-full items-center justify-center content-center"
        ):
            with ui.element("div").classes(
                "flex flex-col h-full w-[60px] "
                "hover:cursor-pointer hover:bg-stone-50/30 rounded-sm"
            ) as player_card_clickable:
                dialog = self.create_player_dialog()
                player_card_clickable.on("click", dialog.open)
                with ui.element("div").classes("grow relative p-1"):
                    ui.image("https://i.ibb.co/zsQThP3/ARS-2223-HK-PL-S1.webp").classes(
                        "border-1 border-black w-full h-full"
                    ).props("fit=scale-down")

                    if self.is_captain:
                        if self.multiplier == 3:
                            ui.icon("local_fire_department").classes(
                                "absolute top-0.5 -right-1"
                            )

                        else:
                            ui.icon("copyright", size="14px").classes(
                                "absolute top-0.5 -right-1"
                            )
                    if not transfer:
                        if self.auto_sub:
                            if self.starting:
                                ui.icon(
                                    "add_circle",
                                    color=Player.team_color[home],
                                    size="14px",
                                ).classes(
                                    "h-[10px] w-[10px] absolute top-0.5 -left-1 "
                                    "bg-white rounded-full"
                                )
                            else:
                                ui.icon(
                                    "do_not_disturb_on",
                                    color=Player.team_color[home],
                                    size="14px",
                                ).classes(
                                    "h-[10px] w-[10px] absolute top-0.5 -left-1 "
                                    "bg-white rounded-full"
                                )

                with ui.element("div").classes("w-full h-[30%]"):
                    ui.label(self.name).classes(
                        player_label
                        + " bg-"
                        + Player.team_color[home]
                        + " text-white rounded-t-sm"
                    ).style(
                        "overflow:hidden;white-space: nowrap;text-overflow: "
                        "ellipsis;display: block;"
                    )

                    ui.label(self.actual_points).classes(
                        player_label + " bg-slate-400/60 text-zinc-900 rounded-b-sm"
                    )

    def transfer_card(self, other_player, home):
        with ui.element("div").classes(
            "w-full flex flex-row justify-center content-center items-center mt-2"
        ).classes("player-card-height"):
            self.create_card(home, True)

            dialog = self.create_transfer_dialog(other_player)

            with ui.column().classes("gap-y-0 items-center"):
                transfer_icon_clickable = ui.icon(
                    "info", size="30px", color=Player.team_color[home]
                ).classes(
                    "hover:cursor-pointer hover:scale-125 bg-stone-100 rounded-full "
                )
                transfer_icon_clickable.on("click", dialog.open)
                ui.icon("swap_horiz", size="40px", color="stone-100").classes("")

            other_player.create_card(home, True)
