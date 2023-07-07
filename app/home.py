#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Callable, List
import requests
from nicegui import ui, Tailwind, app
import pandas as pd
from typing import Self
import asyncio

import fpl_api_getters
from player import Player

from custom_components import input_with_select


from squad_display import show_squad
from search import (
    search,
    manager_id_search_bar,
    top_50_search,
    mini_league_search_bar,
)

card_common_style = (
    "col-span-1 row-span-1 flex justify-center content-center "
    "items-center max-h-[20px]"
)
card_width = " w-[60px]"
card_height = " h-full "
shirt_width = " w-[40px]"

shirt_image_div = (
    "col-span-1 row-span-2 grid-cols-1 grid-rows-1 flex "
    "justify-center items-center relative"
)


player_name_label = (
    "text-black text-center align-middle text-xs md:texts-sm "
    "font-medium overflow-hidden truncate leading-tight "
    "tracking-tighter line-clamp-1"
)

player_points_div = (
    "col-span-1 row-span-1 w-full max-h-[20px] flex justify-center "
    "content-center items-center bg-slate-400/60"
)

player_points_label = (
    "text-white text-center align-top text-xs md:texts-sm "
    "font-medium truncate overflow-hidden leading-tight "
    "tracking-tighter"
)


def row_generator_bench(player_list: List[Player], home: bool):
    with ui.row().classes(
        "flex flex-row  w-full h-full justify-around content-center gap-x-0 "
    ):
        for player in player_list:
            standard_player_card(player, home)


def row_generator(player_list: List[Player], home: bool):
    if home:
        rotate = ""
    else:
        rotate = " rotate-180 lg:rotate-0"

    with ui.row().classes(
        "flex flex-row  w-full h-1/4 justify-around content-start gap-x-0 " + rotate
    ):
        for player in player_list:
            standard_player_card(player, home)


def standard_player_card(player, home: bool):
    with ui.element("div").classes(
        "flex flex-row  flex-1 h-full items-center justify-center content-center"
    ):
        with ui.element("div").classes(
            "grid grid-cols-1 grid-rows-3  h-full" + card_width
        ):
            with ui.element("div").classes(shirt_image_div):
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
                    card_color = " bg-blue-500"
                else:
                    card_color = " bg-red-500"

                with ui.element("div").classes(
                    card_common_style + card_width + card_color
                ):
                    ui.label(player.name).classes(player_name_label)

                with ui.element("div").classes(player_points_div):
                    ui.label(player.actual_points).classes(player_points_label)


def manager_summary(manager_name, points, home: bool):
    if home:
        color = " bg-blue-500 "
    else:
        color = " bg-red-500 "
    with ui.element("div").classes(
        "h-full w-1/2 max-w-[150px] md:max-w-[250px] flex flex-row justify-center "
        "content-start"
    ):
        with ui.element("div").classes(
            "w-full h-[50px] flex flex-row content-center rounded-t-xl" + color
        ):
            ui.label(manager_name).classes(
                "text-center w-full text-lg lg:text-2xl text-white"
            )

        with ui.element("div").classes(
            "w-full h-[100px]  flex flex-row content-center bg-slate-400/60"
        ):
            ui.label(points).classes(
                "text-center w-full text-white text-5xl md:text-7xl"
            )
            ui.label("Points").classes("text-center w-full text-white")


squad_1 = fpl_api_getters.manager_gw_picks_api_temp(38, 13231)
squad_2 = fpl_api_getters.manager_gw_picks_api_temp(38, 1310)

team_1, team_2 = squad_1.compare_squad(squad_2)


def manager_chip(manager_name: str, home: bool):
    if home:
        chip_bg = " bg-blue-400"
    else:
        chip_bg = " bg-red-400"

    with ui.element("div").classes(
        "w-[210px] h-[40px] rounded-lg outline outline-offset-4 "
        "outline-white" + chip_bg
    ) as chip:
        with ui.row().classes(
            "w-full h-full flex flex-row justify-between content-center " "items-center"
        ):
            manager_name = ui.label(manager_name).classes(
                "text-white pl-2 line-clamp-1 max-w-[150px] font-semibold text-md"
            )
            delete_chip = ui.icon("cancel", size="25px").classes(
                "cursor-pointer pr-2 text-slate-50 hover:text-slate-400"
            )

    chip.style("visibility:hidden")

    return chip, manager_name, delete_chip


async def show_page():
    with ui.element("div").classes("flex flex-row"):
        with ui.element("div").classes(
            (
                "flex flex-row justify-center items-center content-center h-screen "
                "w-screen bg-gradient-to-b from-blue-400 via-blue-300 to-white gap-y-0 "
            )
        ):
            with ui.element("div").classes("h-1/4 w-full flex flex-row"):
                ui.label()

            with ui.element("div").classes(
                "h-1/4 w-full flex flex-row justify-center content-end pb-6"
            ):
                ui.label("Compare Squads.").classes(
                    "text-5xl sm:text-5xl text-white font-sans font-bold w-full "
                    "text-center "
                )
            with ui.element("div").classes(
                "h-1/4 w-full flex flex-row content-start justify-center"
            ):
                input_1, gw_select_1 = input_with_select()

                input_1.classes("w-2/3 max-w-[300px]")
                gw_select_1.classes("w-1/3 max-w-[100px]")

                chip_state = {"chip_1": None, "chip_2": None}

                def add_chip(name):
                    if name:
                        if not chip_state["chip_1"]:
                            chip_state["chip_1"] = name
                            chip_1.style("visibility:visible")
                        elif not chip_state["chip_2"]:
                            chip_state["chip_2"] = name
                            chip_2.style("visibility:visible")
                    else:
                        ui.label()

                def delete_chip(chip):
                    if chip == chip_1:
                        chip_state["chip_1"] = None
                    else:
                        chip_state["chip_2"] = None

                    chip.style("visibility:hidden")

                with ui.element("div").classes(
                    "w-full flex flex-row justify-center content-start gap-x-4 gap-y-6 "
                    "pt-6"
                ):
                    chip_1, manager_name_1, delete_chip_1 = manager_chip(
                        "WHU Tang Clan", True
                    )
                    chip_2, manager_name_2, delete_chip_2 = manager_chip(
                        "Ruislip Rejects", False
                    )

                    manager_name_1.bind_text_from(chip_state, "chip_1")
                    manager_name_2.bind_text_from(chip_state, "chip_2")

            with ui.element("div").classes(
                "h-1/4 w-full flex flex-row content-start justify-center"
            ):
                with ui.element("div").classes(
                    "w-full flex flex-row justify-center pt-8 sm:pt-0"
                ):
                    with ui.button().classes("w-[140px] h-[50px]").props(
                        'push color="white" text-color="primary" '
                    ):
                        ui.label("I'm Ready!").classes("text-black text-md")
                        # ui.icon("search", size="30px").classes("text-black")

                # compare_button.style("visibility:hidden")

            delete_chip_1.on("click", lambda x: delete_chip(chip_1))

            delete_chip_2.on("click", lambda x: delete_chip(chip_2))

            input_1.on("keydown.enter", lambda x: add_chip(input_1.value))

        with ui.element("div").classes(
            (
                "flex flex-row justify-center content-center min-h-screen "
                " w-full bg-gradient-to-b from-white from 5% via-green-400 via-10% "
                "to-emerald-500 to-80% gap-y-0 overflow-hidden gap-x-10"
            )
        ):
            with ui.label("").classes(
                "w-full h-[100px] flex flex-row justify-center content-center"
            ):
                ui.button("Change Managers", icon="keyboard_double_arrow_up").classes(
                    "w-full h-[50px] animate-bounce"
                ).props('flat bg-transparent text-color="grey-7"')

            with ui.element("div").classes(
                "w-full h-[150px] flex flex-row justify-evenly content-center mx-2 "
                "lg:gap-x-0 mb-6"
            ):
                manager_summary("Manager 1", "67", True)

                manager_summary("Manager 2", "78", False)

            with ui.element("div").classes(
                "mx-[4px] w-full gap-x-10 flex flex-row justify-center content-center "
                " mb-2"
            ):
                with ui.image(
                    "https://i.ibb.co/xS9j0v0/half-pitch-complete-final-4.png"
                ).classes("max-w-[482px] w-full "):
                    with ui.element("div").classes(
                        "w-full h-full gap-y-1 bg-transparent flex flex-row"
                    ):
                        row_generator(team_1[1], True)
                        row_generator(team_1[2], True)
                        row_generator(team_1[3], True)
                        row_generator(team_1[4], True)

                with ui.image(
                    "https://i.ibb.co/xS9j0v0/half-pitch-complete-final-4.png"
                ).classes("max-w-[482px] w-full rotate-180 lg:rotate-0"):
                    with ui.element("div").classes(
                        "w-full h-full gap-y-1 flex flex-row bg-transparent"
                    ):
                        row_generator(team_1[1], False)
                        row_generator(team_1[2], False)
                        row_generator(team_1[3], False)
                        row_generator(team_1[4], False)

            with ui.element("div").classes(
                "w-full  flex flex-row justify-center content-center gap-x-10 mb-2 "
                "gap-y-2"
            ):
                with ui.element("div").classes(
                    "w-full max-w-[482px] h-[120px] flex flex-row justify-evenly "
                    "content-center"
                ):
                    row_generator_bench(team_1[0], True)
                with ui.element("div").classes(
                    "w-full max-w-[482px] h-[120px] flex flex-row justify-evenly "
                    "content-center"
                ):
                    row_generator_bench(team_1[0], False)
