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

from fpl_api_getters import manager_gw_picks_api
from player import Player
from squad import Squad

card_common_style = (
    "col-span-1 row-span-1 flex justify-center content-center "
    "items-center max-h-[20px]"
)
card_width = " w-[60px] xs:w-[70px] sm:w-[85px] md:w-[100px] lg:w-[115px] "
card_height = " h-full xs:h-[70px] sm:h-[85px] md:h-[100px] lg:h-[115px] "
shirt_width = " w-[30px] xs:w-[40px] sm:w-[50px] md:w-[60px] lg:w-[70px] "

shirt_image_div = (
    "col-span-1 row-span-2 grid-cols-1 grid-rows-1 flex "
    "justify-center items-center relative"
)


player_name_label = (
    "text-white text-center align-middle text-xs md:texts-sm "
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


bench_card_generator_div = (
    "flex flex-row lg:flex-col flex-1 h-full justify-around "
    "content-center items-center gap-x-0"
)


full_bench_div = (
    "grid grid-cols-1 col-span-5 h-[210px] min-h-[190px] sm:h-[250px] "
    "md:h-[300px] lg:h-full lg:col-span-1 border-double border-4 "
    "border-slate-200 rounded-md lg:ml-4 divide-y-4 divide-double"
)

borders = " "


def manager_summary(squad: Squad, home: bool):
    if home:
        color = " bg-blue-500 "
        color_2 = " bg-blue-200 "
        rounding_1 = "rounded-tl-lg lg:rounded-t-lg"
        rounding_2 = "rounded-bl-lg lg:rounded-b-lg"
    else:
        color = " bg-red-500 "
        color_2 = " bg-red-200 "
        rounding_1 = "rounded-tr-lg lg:rounded-t-lg"
        rounding_2 = "rounded-br-lg lg:rounded-b-lg"
    with ui.element("div").classes(
        "grid grid-cols-1 lg:grid-cols-2 w-1/2 lg:w-2/5 lg:max-w-[350px] h-auto "
        "items-center justify-center content-center"
    ):
        with ui.element("div").classes(
            "grid col-span-1 lg:col-span-2 items-center justify-center h-[60px] "
            "lg:h-[80px] content-center " + color + rounding_1
        ):
            ui.label(squad.stats["team_name"]).classes(
                "text-center text-xl lg:text-3xl text-white"
            )
        with ui.element("div").classes(
            "grid grid-cols-1 col-span-1 lg:col-span-2 " + color_2
        ):
            with ui.element("div").classes(
                (
                    "grid grid-cols-1 col-span-1 items-center "
                    "justify-center content-center my-2"
                )
            ):
                ui.label(squad.stats["points"]).classes(
                    "col-span-1 text-center text-6xl text-white"
                )
                ui.label("Points").classes("col-span-1 text-center text-white")
        with ui.element("div").classes(
            (
                "grid col-span-1  lg:col-span-2 items-center justify-center "
                "content-center bg-stone-400  py-1 "
            )
            + rounding_2
        ):
            if squad.chip is None:
                chip_label = "No chip"
            else:
                chip_label = squad.chip
            ui.label(chip_label).classes("text-center text-lg text-white")
        # with ui.element("div").classes("col-span-1"):
        #     ui.label(f"Total points: {squad.stats['total_points']}")
        # with ui.element("div").classes("col-span-1"):
        #     ui.label(f"points on bench: {squad.stats['points_on_bench']}")


def manager_summary_compare(squad_1: Squad, squad_2: Squad):
    with ui.element("div").classes(
        ("col-span-5 flex items-center justify-center content-center w-full")
    ):
        with ui.element("div").classes(
            (
                "flex flex-row flex-1 items-center justify-evenly content-center"
                " p-2 m-2 divide-x-2 divide-white"
            )
        ):
            manager_summary(squad_1, True)

            manager_summary(squad_2, False)


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
                    card_color = "bg-blue-500"
                else:
                    card_color = "bg-red-500"

                with ui.element("div").classes(
                    card_common_style + card_width + card_color
                ):
                    ui.label(player.name).classes(player_name_label)

                with ui.element("div").classes(player_points_div):
                    ui.label(player.actual_points).classes(player_points_label)


def standard_bench_card(player, home: bool):
    with ui.element("div").classes(
        "flex flex-1 h-full lg:w-full items-center justify-center content-center"
    ):
        with ui.element("div").classes(
            "grid grid-cols-1 grid-rows-3  h-full" + card_width
        ):
            with ui.element("div").classes(shirt_image_div):
                ui.image("https://i.ibb.co/zsQThP3/ARS-2223-HK-PL-S1.webp").classes(
                    "cols-span-1 row-span-1 object-contain" + shirt_width
                )
                if player.is_captain:
                    ui.icon("copyright").classes("w-1/5 h-1/5 absolute top-1 right-1")

            with ui.element("div").classes(
                (
                    "col-span-1 row-span-1 grid grid-col-1 grid-rows-2 w-full "
                    "max-h-[40px] pb-2 lg:pb-0"
                )
            ):
                if home:
                    card_color = "bg-blue-500"
                else:
                    card_color = "bg-red-500"

                with ui.element("div").classes(
                    card_common_style + card_width + card_color
                ):
                    ui.label(player.name).classes(player_name_label)

                with ui.element("div").classes(player_points_div):
                    ui.label(player.points).classes(player_points_label)


def row_generator(player_list: List[Player], home: bool):
    with ui.row().classes(
        "flex flex-row  w-full h-1/4 justify-around content-center gap-x-0"
    ):
        for player in player_list:
            standard_player_card(player, home)


def row_generator_bench(player_list: List[Player], home: bool, chip):
    if (chip is not None) and (chip == "bboost"):
        with ui.row().classes(bench_card_generator_div + "bg-green-100"):
            for player in player_list:
                standard_bench_card(player, home)
    else:
        with ui.row().classes(bench_card_generator_div):
            for player in player_list:
                standard_bench_card(player, home)


async def show_squad(
    tab,
    complete_div,
    error_message,
    manager_id_1: int,
    manager_id_2: int,
    gameweek: int,
):
    complete_div.clear()
    error_message.clear()

    squad_1 = manager_gw_picks_api(gameweek, manager_id_1)
    squad_2 = manager_gw_picks_api(gameweek, manager_id_2)
    if squad_1 is None:
        ui.notify(
            f"Manager ID 1 does not exist on gameweek {gameweek}",
            type="negative",
            position="center",
        )
        return

    if squad_2 is None:
        ui.notify(
            f"Manager ID 2 does not exist on gameweek {gameweek}",
            type="negative",
            position="center",
        )
        return

    team_1, team_2 = squad_1.compare_squad(squad_2)

    with tab:
        with ui.element("div").classes(
            (
                "flex flex-row w-full h-full absolute top-0 left-0 bg-stone-200/50 "
                "items-center justify-center content-center"
            )
        ) as spinner_div:
            ui.spinner(size="xl")
    await asyncio.sleep(2)

    with complete_div.classes("flex flex-row justify-center "):
        with ui.element("div").classes(
            "w-full h-full max-w-[1000px] grid grid-cols-5 justify-center "
        ):
            manager_summary_compare(squad_1, squad_2)
            with ui.element("div").classes("col-span-5 lg:h-full lg:col-span-4"):
                with ui.image("https://i.ibb.co/9WbhshN/pitch.jpg").classes(
                    "w-full h-full rounded-2xl mb-4"
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

            with ui.element("div").classes(full_bench_div):
                with ui.element("div").classes(
                    "col-span-1 min-h-[100px] h-full flex flex-col grow"
                ):
                    row_generator_bench(team_1[0], True, squad_1.chip)

                with ui.element("div").classes("col-span-1 min-h-[100px]"):
                    row_generator_bench(team_2[0], False, squad_2.chip)

    tab.remove(spinner_div)

    return complete_div
