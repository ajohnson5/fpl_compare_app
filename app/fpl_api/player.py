from nicegui import ui

player_label = "w-full h-1/2 justify-center content-center items-center flex flex-row "
card_width = " w-[60px]"
shirt_image_div = (
    "col-span-1 row-span-2 grid-cols-1 grid-rows-1 flex "
    "justify-center items-center relative"
)


class Player:
    team_color = {"home": "sky-500", "away": "red-500"}

    team_images = {
        "Arsenal": "https://i.ibb.co/BBZLt6S/arsenal.png",
        "Aston Villa": "https://i.ibb.co/6Z0C37X/aston-villa.png",
        "Bournemouth": "https://i.ibb.co/6t8HvvY/bournemouth.png",
        "Brentford": "https://i.ibb.co/CJ0sMbx/brentford.png",
        "Brighton": "https://i.ibb.co/NL8jLg9/brighton.png",
        "Burnley": "https://i.ibb.co/VQQX3R7/burnley.png",
        "Chelsea": "https://i.ibb.co/4mdD3dX/chelsea.png",
        "Crystal Palace": "https://i.ibb.co/31FRWGM/crystal-palace.png",
        "Everton": "https://i.ibb.co/F3Y6tKb/everton.png",
        "Fulham": "https://i.ibb.co/nDzqGf3/fulham.png",
        "Liverpool": "https://i.ibb.co/t3MxJYt/liverpool.png",
        "Luton": "https://i.ibb.co/bJFTv6W/luton-town.png",
        "Man City": "https://i.ibb.co/ch7KS2X/manchester-city.png",
        "Man Utd": "https://i.ibb.co/F8Cp5ht/manchester-united.png",
        "Newcastle": "https://i.ibb.co/6yyK28z/newcastle-united.png",
        "Nott'm Forest": "https://i.ibb.co/fkjLr13/nottingham-forest.png",
        "Sheffield Utd": "https://i.ibb.co/89LX84X/sheffield-united.png",
        "Spurs": "https://i.ibb.co/FnLrrPV/tottenham-hotspur.png",
        "West Ham": "https://i.ibb.co/LnfvdzS/wolverhampton-wanders.png",
        "Wolves": "https://i.ibb.co/MB18mXz/west-ham-united.png",
    }

    def __init__(
        self,
        id: int,
        second_name: str,
        first_name: str,
        web_name: str,
        position: int,
        team_name: str,
        cost: int,
    ):
        self.id = id
        self.second_name = second_name
        self.first_name = first_name
        self.web_name = web_name
        self.position = position
        self.team_name = team_name
        self.cost = cost

    def __eq__(self, other):
        if self.id == other.id:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.id, self.position))

    def __bool__(self):
        return self.id is not None  # <--- added "return"

    def create_card(self):
        with ui.element("div").classes(
            "flex flex-row  flex-1 h-full items-center justify-center content-center"
        ):
            with ui.element("div").classes(
                "flex flex-col h-full w-[60px] "
                "hover:cursor-pointer hover:bg-stone-50/30 rounded-sm transition-colors"
            ):
                # dialog = self.create_player_dialog()
                # player_card_clickable.on("click", dialog.open)
                with ui.element("div").classes("grow relative p-1"):
                    ui.image(Player.team_images[self.team_name]).classes(
                        "border-1 border-black w-full h-full"
                    ).props("fit=scale-down")

                with ui.element("div").classes("w-full h-[35%]"):
                    with ui.element("div").classes(
                        player_label + " rounded-t-sm bg-" + Player.team_color["home"]
                    ):
                        ui.label(self.web_name).classes(
                            "h-auto w-full text-center font-medium tracking-tighter "
                            "text-white text-xs leading-none "
                        ).style(
                            "overflow:hidden;white-space: nowrap;text-overflow: "
                            "ellipsis;display: block; "
                        )

                    with ui.element("div").classes(
                        player_label + " rounded-t-sm bg-slate-400/60 rounded-b-sm"
                    ):
                        ui.label(self.cost).classes(
                            "h-auto text-center text-xs font-medium tracking-tighter "
                            "text-zinc-900 leading-none"
                        )


class PlayerGameweek(Player):
    def __init__(
        self,
        id: int,
        second_name: str,
        first_name: str,
        web_name: str,
        squad_order: int,
        position: int,
        total_points: int,
        points: int,
        bonus_points: int,
        minutes: int,
        team_name: str,
        is_captain: bool,
        multiplier: int,
        auto_sub: bool,
        transfer: int,
        cost: int,
    ):
        super().__init__(
            id,
            second_name,
            first_name,
            web_name,
            position,
            team_name,
            cost,
        )
        self.squad_order = squad_order
        self.starting = squad_order <= 11
        self.total_points = total_points
        self.points = points
        self.actual_points = points * multiplier if multiplier else points
        self.bonus_points = bonus_points
        self.minutes = minutes
        self.is_captain = is_captain
        self.multiplier = multiplier
        self.auto_sub = auto_sub
        self.transfer = transfer

    def create_player_dialog(
        self,
    ):
        with ui.dialog() as dialog, ui.card().classes("relative w-72 min-h-48"):
            ui.label(f"{self.first_name} {self.second_name}").classes(
                "w-full h-auto text-center text-lg text-zinc-900 font-medium font-sans "
                "align-middle"
            )
            ui.separator()

            with ui.element("div").classes("w-full h-auto flex flex-row"):
                with ui.element("div").classes("w-1/2 h-auto p-2"):
                    ui.label("Season Points").classes(
                        "text-start align-middle text-md pb-2"
                    )
                    ui.label("Bonus Points").classes("text-start align-middle pb-2")
                    ui.label("Minutes").classes("text-start align-middle")

                with ui.element("div").classes("w-1/2 p-2"):
                    ui.label(self.total_points).classes("text-center align-middle pb-2")
                    ui.label(self.bonus_points).classes("text-center align-middle pb-2")
                    ui.label(self.minutes).classes("text-center align-middle")

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

            with ui.element("div").classes("w-full h-auto flex flex-row"):
                with ui.element("div").classes("w-1/2 h-auto p-2"):
                    ui.label("Transfer Cost").classes(
                        "text-start align-middle text-md pb-2"
                    )
                    ui.label("Transfer Revenue").classes("text-start align-middle pb-2")
                    ui.label("Point Profit").classes("text-start align-middle")

                with ui.element("div").classes("w-1/2 p-2"):
                    ui.label(self.transfer["element_in_cost"]).classes(
                        "text-center align-middle pb-2"
                    )
                    ui.label(self.transfer["element_out_cost"]).classes(
                        "text-center align-middle pb-2"
                    )
                    ui.label(self.actual_points - other_player.actual_points).classes(
                        "text-center align-middle"
                    )

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
                "hover:cursor-pointer hover:bg-stone-50/30 rounded-sm transition-colors"
            ) as player_card_clickable:
                dialog = self.create_player_dialog()
                player_card_clickable.on("click", dialog.open)
                with ui.element("div").classes("grow relative p-1"):
                    ui.image(Player.team_images[self.team_name]).classes(
                        "border-1 border-black w-full h-full"
                    ).props("fit=scale-down")

                    if self.is_captain:
                        if self.multiplier == 3:
                            ui.icon(
                                "local_fire_department", size="10px", color="stone-100"
                            ).classes(
                                "h-[13px] w-[13px] absolute top-0.5 right-0 "
                                "rounded-full bg-" + Player.team_color[home]
                            )

                        else:
                            ui.icon(
                                "copyright", size="14px", color="stone-100"
                            ).classes(
                                "h-[10px] w-[10px] absolute top-0.5 right-0 "
                                "rounded-full bg-" + Player.team_color[home]
                            )
                    if not transfer:
                        if self.auto_sub:
                            if self.starting:
                                ui.icon(
                                    "add_circle",
                                    color=Player.team_color[home],
                                    size="14px",
                                ).classes(
                                    "h-[10px] w-[10px] absolute top-0.5 left-0 "
                                    "bg-white rounded-full"
                                )
                            else:
                                ui.icon(
                                    "do_not_disturb_on",
                                    color=Player.team_color[home],
                                    size="14px",
                                ).classes(
                                    "h-[10px] w-[10px] absolute top-0.5 left-0 "
                                    "bg-white rounded-full"
                                )

                with ui.element("div").classes("w-full h-[35%]"):
                    with ui.element("div").classes(
                        player_label + " rounded-t-sm bg-" + Player.team_color[home]
                    ):
                        ui.label(self.web_name).classes(
                            "h-auto w-full text-center font-medium tracking-tighter "
                            "text-white text-xs leading-none "
                        ).style(
                            "overflow:hidden;white-space: nowrap;text-overflow: "
                            "ellipsis;display: block; "
                        )

                    with ui.element("div").classes(
                        player_label + " rounded-t-sm bg-slate-400/60 rounded-b-sm"
                    ):
                        ui.label(self.actual_points).classes(
                            "h-auto text-center text-xs font-medium tracking-tighter "
                            "text-zinc-900 leading-none"
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
                    "hover:cursor-pointer hover:scale-125 rounded-full "
                    "transition bg-stone-100 w-[10px] h-[20px]"
                )
                transfer_icon_clickable.on("click", dialog.open)
                ui.icon("swap_horiz", size="40px", color="stone-100").classes("")

            other_player.create_card(home, True)
