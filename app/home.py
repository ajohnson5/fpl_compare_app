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
from generate_squad import generate_squad

from squad_display import show_squad
from search import (
    search,
    manager_id_search_bar,
    top_50_search,
    mini_league_search_bar,
)


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
        ) as landing_div:
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

                def add_chip(manager_id, gw_select_1):
                    if manager_id and gw_select_1:
                        if not chip_state["chip_1"]:
                            manager_name = fpl_api_getters.manager_name(manager_id)
                            if manager_name:
                                chip_state["chip_1"] = manager_name
                                chip_1.style("visibility:visible")
                            else:
                                ui.notify("Manager does not exist", closeBtn="OK")
                        elif not chip_state["chip_2"]:
                            manager_name = fpl_api_getters.manager_name(manager_id)
                            if manager_name:
                                chip_state["chip_2"] = manager_name
                                chip_2.style("visibility:visible")
                            else:
                                ui.notify("Manager does not exist", closeBtn="OK")
                    else:
                        pass

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

            async def manager_id_search():
                if chip_state["chip_1"] and chip_state["chip_2"]:
                    await generate_squad(
                        chip_state["chip_1"],
                        chip_state["chip_2"],
                        38,
                        38,
                        display_div,
                        landing_div,
                        manager_summary_div,
                        squad_1_display,
                        squad_2_display,
                        bench_1_display,
                        bench_2_display,
                    )
                else:
                    ui.notify("Please enter 2 manager IDs", closeBtn="OK")

            with ui.element("div").classes(
                "h-1/4 w-full flex flex-row content-start justify-center"
            ):
                with ui.element("div").classes(
                    "w-full flex flex-row justify-center pt-8 sm:pt-0"
                ):
                    ui.button("I'm Ready!", on_click=manager_id_search).classes(
                        "w-[140px] h-[50px]"
                    ).props('push color="white" text-color="blue-5" ')

            # compare_button.style("visibility:hidden")

            delete_chip_1.on("click", lambda x: delete_chip(chip_1))

            delete_chip_2.on("click", lambda x: delete_chip(chip_2))

            input_1.on(
                "keydown.enter", lambda x: add_chip(input_1.value, gw_select_1.value)
            )

        with ui.element("div").classes(
            (
                "flex flex-row justify-center content-center min-h-screen "
                " w-full bg-gradient-to-b from-white from 5% via-green-400 via-10% "
                "to-emerald-500 to-80% gap-y-0 overflow-hidden gap-x-10"
            )
        ) as display_div:
            with ui.label("").classes(
                "w-full h-[100px] flex flex-row justify-center content-center"
            ):
                ui.button("Change Managers", icon="keyboard_double_arrow_up").classes(
                    "w-full h-[50px] animate-bounce"
                ).props('flat bg-transparent text-color="grey-7"')

            manager_summary_div = ui.element("div").classes(
                "w-full h-[150px] flex flex-row justify-evenly content-center mx-2 "
                "lg:gap-x-0 mb-6"
            )
            with ui.element("div").classes(
                "mx-[4px] w-full gap-x-10 flex flex-row justify-center content-center "
                " mb-2"
            ):
                with ui.image(
                    "https://i.ibb.co/xS9j0v0/half-pitch-complete-final-4.png"
                ).classes("max-w-[482px] w-full "):
                    squad_1_display = ui.element("div").classes(
                        "w-full h-full gap-y-1 bg-transparent flex flex-row"
                    )

                with ui.image(
                    "https://i.ibb.co/xS9j0v0/half-pitch-complete-final-4.png"
                ).classes("max-w-[482px] w-full rotate-180 lg:rotate-0"):
                    squad_2_display = ui.element("div").classes(
                        "w-full h-full gap-y-1 flex flex-row bg-transparent"
                    )
            with ui.element("div").classes(
                "w-full  flex flex-row justify-center content-center gap-x-10 mb-2 "
                "mx-2 gap-y-2"
            ):
                bench_1_display = ui.element("div").classes(
                    "w-full max-w-[482px] h-[120px] flex flex-row justify-evenly "
                    "content-center border-2     border-white"
                )

                bench_2_display = ui.element("div").classes(
                    "w-full max-w-[482px] h-[120px] flex flex-row justify-evenly "
                    "content-center border-2 border-white "
                )

        display_div.set_visibility(False)
