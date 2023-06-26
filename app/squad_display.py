#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Callable, List
import requests
from nicegui import ui, Tailwind, app
import pandas as pd
from itertools import zip_longest
from typing import Self
import asyncio


from fpl_api_getters import manager_gw_picks_api
from player import Player
from squad import Squad


card_width = " w-[60px] xs:w-[70px] sm:w-[85px] md:w-[100px] lg:w-[115px] "
card_height = " h-full xs:h-[70px] sm:h-[85px] md:h-[100px] lg:h-[115px] "
shirt_width = " w-[30px] xs:w-[40px] sm:w-[50px] md:w-[60px] lg:w-[70px] "


def standard_player_card(player, home: bool):
    with ui.element("div").classes(
        "flex flex-row  flex-1 h-full items-center justify-center content-center"
    ):
        with ui.element("div").classes(
            "grid grid-cols-1 grid-rows-3  h-full" + card_width
        ):
            with ui.element("div").classes(
                "col-span-1 row-span-2 grid-cols-1 grid-rows-1  flex justify-center items-center relative"
            ):
                ui.image("https://i.ibb.co/zsQThP3/ARS-2223-HK-PL-S1.webp").classes(
                    "cols-span-1 row-span-1 object-contain" + shirt_width
                )

                if player.is_captain:
                    if player.multiplier == 3:
                        ui.icon("local_fire_department").classes(
                            "w-1/5 h-1/5 absolute top-1 right-1"
                        )

                    else:
                        ui.icon("copyright").classes(
                            "w-1/5 h-1/5 absolute top-1 right-1"
                        )

            with ui.element("div").classes(
                "col-span-1 row-span-1 grid grid-col-1 grid-rows-2 w-full max-h-[40px]"
            ):
                if home:
                    card_color = "bg-blue-500"
                else:
                    card_color = "bg-red-500"

                with ui.element("div").classes(
                    "col-span-1 row-span-1 flex justify-center content-center items-center max-h-[20px]"
                    + card_width
                    + card_color
                ):
                    ui.label(player.name).classes(
                        "text-white text-center align-middle text-xs md:texts-sm font-medium overflow-hidden truncate leading-tight tracking-tighter line-clamp-1"
                    )

                with ui.element("div").classes(
                    "col-span-1 row-span-1 w-full max-h-[20px] flex justify-center content-center items-center bg-slate-400/60"
                ):
                    ui.label(player.actual_points).classes(
                        "text-white text-center align-top text-xs md:texts-sm font-medium truncate overflow-hidden leading-tight tracking-tighter "
                    )


def standard_bench_card(player, home: bool):
    with ui.element("div").classes(
        "flex flex-grow flex-1 h-full lg:w-full  items-center justify-center content-center"
    ):
        with ui.element("div").classes(
            "grid grid-cols-1 grid-rows-3  h-full" + card_width
        ):
            with ui.element("div").classes(
                "col-span-1 row-span-2 grid-cols-1 grid-rows-1  flex justify-center items-center relative"
            ):
                ui.image("https://i.ibb.co/zsQThP3/ARS-2223-HK-PL-S1.webp").classes(
                    "cols-span-1 row-span-1 object-contain" + shirt_width
                )
                if player.is_captain:
                    ui.icon("copyright").classes("w-1/5 h-1/5 absolute top-1 right-1")

            with ui.element("div").classes(
                "col-span-1 row-span-1 grid grid-col-1 grid-rows-2 w-full max-h-[40px] pb-2 lg:pb-0"
            ):
                if home:
                    card_color = "bg-blue-500"
                else:
                    card_color = "bg-red-500"

                with ui.element("div").classes(
                    "col-span-1 row-span-1 flex justify-center content-center items-center max-h-[20px]"
                    + card_width
                    + card_color
                ):
                    ui.label(player.name).classes(
                        "text-white text-center align-middle text-xs md:texts-sm font-medium overflow-hidden truncate leading-tight tracking-tighter line-clamp-1"
                    )

                with ui.element("div").classes(
                    "col-span-1 row-span-1 w-full max-h-[20px] flex justify-center content-center items-center bg-slate-400/60"
                ):
                    ui.label(player.points).classes(
                        "text-white text-center align-top text-xs md:texts-sm font-medium truncate overflow-hidden leading-tight tracking-tighter "
                    )


def row_generator(player_list: List[Player], home: bool):
    with ui.row().classes(
        "flex flex-row  w-full h-1/4 justify-around content-center gap-x-0"
    ):
        # with ui.row().classes('w-full h-1/4 grid-cols-5 justify-around w-full gap-x-0.5 content-center') as tester:
        for player in player_list:
            standard_player_card(player, home)


def row_generator_bench(player_list: List[Player], home: bool, chip):
    if (chip is not None) and (chip == "bboost"):
        with ui.row().classes(
            "flex flex-row lg:flex-col flex-1 h-full justify-around content-center items-center gap-x-0 bg-green-100"
        ):
            for player in player_list:
                standard_bench_card(player, home)
    else:
        with ui.row().classes(
            "flex flex-row lg:flex-col flex-1 h-full justify-around content-center items-center gap-x-0"
        ):
            for player in player_list:
                standard_bench_card(player, home)


def show_squad(
    complete_div, error_message, manager_id: str, manager_id_2: str, gameweek: int
):
    complete_div.clear()
    error_message.clear()

    squad_1 = manager_gw_picks_api(gameweek, manager_id)
    if squad_1 is None:
        with error_message:
            ui.label("Manager ID 1 does not exist or is an invalid ID.")
        return

    squad_2 = manager_gw_picks_api(gameweek, manager_id_2)
    if squad_2 is None:
        with error_message:
            ui.label("Manager ID 2 does not exist or is an invalid ID.")
        return

    if not squad_1.start_xi:
        ui.label("Squad is empty for given gameweek").classes("mx-auto")
        return

    team_1, team_2 = squad_1.compare_squad(squad_2)

    with complete_div.classes("flex flex-row justify-center "):
        with ui.element("div").classes(
            "w-full h-full max-w-[1000px] grid grid-cols-5 "
        ):
            with ui.element("div").classes("col-span-5 lg:h-full lg:col-span-4"):
                with ui.image("https://i.ibb.co/9WbhshN/pitch.jpg").classes(
                    "w-full h-full"
                ):
                    with ui.element("div").classes("w-full h-full grid-cols-1").style(
                        "background: transparent;"
                    ):
                        with ui.element("div").classes("w-full h-1/2").style(
                            "background: transparent;"
                        ):
                            row_generator(team_1[1], True)
                            row_generator(team_1[2], True)
                            row_generator(team_1[3], True)
                            row_generator(team_1[4], True)

                        with ui.element("div").classes("w-full h-1/2").style(
                            "background: transparent;"
                        ):
                            row_generator(team_2[4], False)
                            row_generator(team_2[3], False)
                            row_generator(team_2[2], False)
                            row_generator(team_2[1], False)

            with ui.element("div").classes(
                "grid grid-cols-1 col-span-5 h-[210px] min-h-[190px] sm:h-[250px] md:h-[300px] lg:h-full lg:col-span-1 border-double border-4 border-slate-200 rounded-md  lg:ml-4 divide-y-4 divide-double"
            ):
                with ui.element("div").classes(
                    "col-span-1 min-h-[100px] h-full flex flex-col grow "
                ):
                    row_generator_bench(team_1[0], True, squad_1.chip)

                with ui.element("div").classes("col-span-1 min-h-[100px]"):
                    row_generator_bench(team_2[0], False, squad_2.chip)

            # with ui.element('div').classes('flex flex-col flex-1 w-full lg:w-1/5 bg-green-500') as bench_container:
            #     with ui.element('div').classes('flex-1 w-full  border-double border-4 border-slate-200 rounded-md divide-y-2 divide-double') as bench:
            #         with ui.element('div').classes('w-full h-1/2 bg-purple-200 ') as bench_home:
            #             row_generator_bench(team_1[0],True)

            #         with ui.element('div').classes('w-full h-1/2 min-h-[100px]') as bench_away:
            #             row_generator_bench(team_2[0],False)

    return complete_div
