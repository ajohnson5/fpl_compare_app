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

from custom_components import input_with_select, league_search
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
        "outline-white relative" + chip_bg
    ) as chip:
        gw_chip_label = ui.label("21").classes(
            "w-[22px] h-[22px] rounded-full "
            "bg-slate-600 text-white absolute -top-[13px] -left-[10px] text-center "
            "font-semibold align-middle"
        )
        with ui.row().classes(
            "w-full h-full flex flex-row justify-between content-center items-center"
        ):
            manager_name = ui.label(manager_name).classes(
                "text-white pl-2 max-w-[150px] h-[20px] font-semibold text-md"
            )
            delete_chip = ui.icon("cancel", size="25px").classes(
                "cursor-pointer pr-2 text-slate-50 hover:text-slate-400"
            )

    chip.style("visibility:hidden")

    return chip, manager_name, delete_chip, gw_chip_label


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
                    "text-4xl sm:text-5xl text-white font-sans font-bold w-full "
                    "text-center "
                )

            search_toggle = (
                ui.switch()
                .classes("absolute top-[85vh] right-[5px]")
                .props('size="70px"')
            )
            with ui.element("div").classes(
                "h-1/4 w-full flex flex-row content-start justify-center relative mx-2"
            ):
                input_1, gw_select_1 = input_with_select()

                input_1.classes("flex-grow min-w-[100px]")
                gw_select_1.classes("w-[60px] sm:w-[80px]")

                (
                    league_input,
                    manager_select_input,
                    gw_select_2,
                    league_search_div,
                ) = league_search()

                gw_select_2.classes("w-[60px] sm:w-[80px]")
                manager_select_input.classes("w-2/5 flex-grow")
                league_input.classes("w-2/5 flex-grow")

                league_search_div.classes("absolute top-0 z-100")
                gw_select_2.bind_visibility_from(search_toggle, "value")
                league_input.bind_visibility_from(search_toggle, "value")
                manager_select_input.bind_visibility_from(search_toggle, "value")

                async def search_league(league_id):
                    if not league_id:
                        with league_input.add_slot("prepend"):
                            with ui.icon("error", color="red-500"):
                                ui.tooltip("Please enter a League ID").classes(
                                    "bg-red-500"
                                )
                            league_input.update()
                        return

                    manager_select_input.clear()

                    manager_select_input.set_value(value=None)

                    managers = await fpl_api_getters.get_mini_league_managers(
                        int(league_id)
                    )

                    managers = {
                        12313: "Ujedinjeni Urci",
                        2131: "Badger Oblong Quasi",
                        3763: "Bad Team On Paper",
                    }

                    if managers:
                        with league_input.add_slot("prepend"):
                            ui.icon("check_circle", color="green-500")
                            league_input.update()
                    else:
                        with league_input.add_slot("prepend"):
                            with ui.icon("error", color="red-500"):
                                ui.tooltip("Invalid League ID").classes("bg-red-500")
                            league_input.update()
                        return

                    manager_select_input.options = managers
                    manager_select_input.update()

                league_input.on(
                    "keydown.enter", lambda: search_league(league_input.value)
                )

                gw_select_1.bind_value(gw_select_2, "value")

                chip_state = {
                    "chip_1": None,
                    "chip_2": None,
                    "chip_1_id": None,
                    "chip_2_id": None,
                    "chip_1_gw": None,
                    "chip_2_gw": None,
                }

                def add_chip(manager_id, gw_select_1):
                    if manager_id and gw_select_1:
                        if not chip_state["chip_1"]:
                            manager_name = fpl_api_getters.manager_name(manager_id)
                            if manager_name:
                                chip_state["chip_1_id"] = int(manager_id)
                                chip_state["chip_1"] = manager_name
                                chip_state["chip_1_gw"] = gw_select_1
                                chip_1.style("visibility:visible")
                            else:
                                ui.notify("Manager does not exist", closeBtn="OK")
                        elif not chip_state["chip_2"]:
                            manager_name = fpl_api_getters.manager_name(manager_id)
                            if manager_name:
                                chip_state["chip_2_id"] = int(manager_id)
                                chip_state["chip_2"] = manager_name
                                chip_state["chip_2_gw"] = gw_select_1
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
                    (
                        chip_1,
                        manager_name_1,
                        delete_chip_1,
                        gw_chip_label_1,
                    ) = manager_chip("WHU Tang Clan", True)
                    (
                        chip_2,
                        manager_name_2,
                        delete_chip_2,
                        gw_chip_label_2,
                    ) = manager_chip("Ruislip Rejects", False)

                    gw_chip_label_1.bind_text_from(chip_state, "chip_1_gw")
                    gw_chip_label_2.bind_text_from(chip_state, "chip_2_gw")

                    manager_name_1.bind_text_from(chip_state, "chip_1")
                    manager_name_2.bind_text_from(chip_state, "chip_2")

            async def manager_id_search():
                if chip_state["chip_1"] and chip_state["chip_2"]:
                    await generate_squad(
                        chip_state,
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

            manager_select_input.on(
                "update:model-value",
                lambda x: add_chip(manager_select_input.value, gw_select_2.value),
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
                    "w-full h-[50px]"
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
