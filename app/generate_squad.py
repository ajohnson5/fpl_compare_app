#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Callable, List
import requests
from nicegui import ui, Tailwind, app
import pandas as pd
from itertools import zip_longest
from typing import Self
import asyncio
import time


import fpl_api_getters
from fpl_api_getters import manager_gw_picks_api
from player import Player
from squad import Squad


card_common_style = (
    "col-span-1 row-span-1 flex justify-center content-center "
    "items-center max-h-[20px]"
)
card_width = " w-[60px]"
card_height = " h-full "
shirt_width = " w-[35px] sm:w-[40px] "

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
        "flex flex-row  w-full h-full justify-around content-center gap-x-0 mb-4"
    ):
        for player in player_list:
            standard_player_card(player, home)


def row_generator(player_list: List[Player], home: bool, i):
    if i == 0:
        x = "top-0"
    else:
        x = f"top-{i}/4"
    if home:
        rotate = "left-0 " + x
    else:
        rotate = " rotate-180 lg:rotate-0 left-0 " + x

    with ui.element("div").classes(
        "flex flex-row absolute w-full h-1/4 justify-around content-start gap-x-0 "
        + rotate
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
                    card_color = " bg-sky-500"
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
        bg_color = " from-sky-500 via-sky-300 to-cyan-400 lg:mr-6"
    else:
        bg_color = " from-red-500 via-red-400 to-rose-400 lg:ml-6"
    with ui.element("div").classes(
        " p-1 bg-gradient-to-r rounded-2xl drop-shadow-xl" + bg_color
    ):
        with ui.element("div").classes(
            "h-full w-[150px] md:w-[250px] flex flex-row justify-center "
            "content-start gap-y-1"
        ):
            with ui.element("div").classes(
                "w-full h-[50px] flex flex-row content-center rounded-t-xl bg-slate-50"
            ):
                ui.label(manager_name).classes(
                    "text-center w-full text-lg lg:text-2xl text-zinc-800 font-medium"
                )

            with ui.element("div").classes(
                "w-full h-[100px]  flex flex-row content-center bg-slate-50 "
                "rounded-b-xl"
            ):
                ui.label(points).classes(
                    "text-center w-full text-zinc-800 text-5xl md:text-7xl font-medium"
                )
                ui.label("Points").classes("text-center w-full text-zinc-800")


async def generate_squad(
    manager_dict,
    display_div,
    loading_div,
    manager_summary_div,
    squad_1_display,
    squad_2_display,
    bench_1_display,
    bench_2_display,
):
    squad_1 = fpl_api_getters.manager_gw_picks_api_temp(38, manager_dict["chip_1_id"])
    squad_2 = fpl_api_getters.manager_gw_picks_api_temp(38, manager_dict["chip_2_id"])

    team_1, team_2 = squad_1.compare_squad(squad_2)

    with loading_div:
        with ui.element("div") as loading_clearable_div:
            with ui.element("div").classes(
                (
                    "flex flex-row w-full h-full fixed top-0 left-0 bg-stone-200/50 "
                    "items-center justify-center content-center backdrop-blur-sm z-50"
                )
            ):
                ui.spinner(size="xl", thickness=10.0)
    await asyncio.sleep(2)
    loading_clearable_div.clear()

    with manager_summary_div:
        manager_summary_div.clear()
        manager_summary(manager_dict["chip_1"], "67", True)

        manager_summary(manager_dict["chip_2"], "78", False)

    with squad_1_display:
        squad_1_display.clear()

        row_generator(team_1[1], True, 0)
        row_generator(team_1[2], True, 1)
        row_generator(team_1[3], True, 2)
        row_generator(team_1[4], True, 3)

    with squad_2_display:
        squad_2_display.clear()
        row_generator(team_1[1], False, 0)
        row_generator(team_1[2], False, 1)
        row_generator(team_1[3], False, 2)
        row_generator(team_1[4], False, 3)

    with bench_1_display:
        bench_1_display.clear()
        row_generator_bench(team_1[0], True)

    with bench_2_display:
        bench_2_display.clear()
        row_generator_bench(team_1[0], False)

    display_div.set_visibility(True)
