from nicegui import ui

player_label = (
    "w-full h-1/2 text-center align-middle "
    "text-xs md:text-sm font-medium tracking-tighter leading-tight "
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
        self.actual_points = points * multiplier
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

    def create_card(self, home, transfer=False):
        with ui.element("div").classes(
            "flex flex-row  flex-1 h-full items-center justify-center content-center"
        ):
            with ui.element("div").classes("flex flex-col h-full w-[60px]"):
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

                with ui.element("div").classes("w-full h-[27px] sm:h-[35px]"):
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
            "w-full flex flex-row justify-center content-center " "items-center mt-2"
        ).classes("player-card-height"):
            self.create_card(home, True)

            ui.icon("swap_horiz", size="50px", color="stone-100")

            other_player.create_card(home, True)
