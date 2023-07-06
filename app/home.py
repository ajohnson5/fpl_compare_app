#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Callable, List
import requests
from nicegui import ui, Tailwind, app
import pandas as pd
from typing import Self
import asyncio

from custom_components import input_with_select


from squad_display import show_squad
from search import (
    search,
    manager_id_search_bar,
    top_50_search,
    mini_league_search_bar,
)


def manager_chip(manager_name: str, home: bool):
    if home:
        chip_bg = " bg-blue-500"
    else:
        chip_bg = " bg-red-500"

    with ui.element("div").classes(
        "w-[210px] h-[40px] rounded-lg outline outline-offset-4 "
        "outline-white" + chip_bg
    ) as chip:
        with ui.row().classes(
            "w-full h-full flex flex-row justify-between content-center " "items-center"
        ):
            manager_name = ui.label(manager_name).classes(
                "text-white pl-2 line-clamp-1 max-w-[150px]"
            )
            delete_chip = ui.icon("cancel", size="25px").classes(
                "cursor-pointer pr-2 text-slate-50 hover:text-slate-400"
            )

    chip.style("visibility:hidden")

    return chip, manager_name, delete_chip


async def show_page():
    with ui.element("div").classes(
        (
            "flex flex-row justify-center items-center content-center h-screen "
            "w-screen bg-gradient-to-b from-blue-400 via-blue-300 to-white"
        )
    ):
        ui.label("Compare Squads.").classes(
            "text-4xl sm:text-5xl text-white font-sans font-bold w-full text-center "
            "mb-8"
        )

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
            "w-full flex flex-row justify-center content-center gap-x-4 gap-y-6 pt-6"
        ):
            chip_1, manager_name_1, delete_chip_1 = manager_chip("WHU Tang Clan", True)
            chip_2, manager_name_2, delete_chip_2 = manager_chip(
                "Ruislip Rejects", False
            )

            manager_name_1.bind_text_from(chip_state, "chip_1")
            manager_name_2.bind_text_from(chip_state, "chip_2")

        delete_chip_1.on("click", lambda x: delete_chip(chip_1))

        delete_chip_2.on("click", lambda x: delete_chip(chip_2))

        input_1.on("keydown.enter", lambda x: add_chip(input_1.value))

        # chip_1.classes("-z-10")

        with ui.element("div").classes("w-full flex flex-row justify-center pt-6"):
            with ui.button().classes("w-[170px] h-[50px]").props(
                'rounded color="white" '
            ) as compare_button:
                ui.label("Compare").classes("text-black text-md")
                ui.icon("change_circle", size="35px").classes("text-black")

        compare_button.style("visibility:hidden")

    #         with ui.tabs().classes("text-blue-4") as tabs:
    #             manager_id_search_tab = ui.tab("Manager ID").classes(
    #                 " rounded-tl-lg w-1/3 "
    #             )
    #             mini_league_search_tab = ui.tab("Mini League").classes("w-1/3")
    #             top_5_search_tab = ui.tab("Top 50").classes("rounded-tr-lg w-1/3")
    #         with ui.tab_panels(
    #             tabs, value=manager_id_search_tab, animated=False
    #         ).classes("w-full h-[200px] rounded-b-lg"):
    #             with ui.tab_panel(manager_id_search_tab):
    #                 (
    #                     manager_id_1_tab_1,
    #                     manager_id_2_tab_1,
    #                     gameweek_tab_1,
    #                     search_button_tab_1,
    #                 ) = manager_id_search_bar()
    #             with ui.tab_panel(mini_league_search_tab):
    #                 (
    #                     manager_id_1_tab_2,
    #                     manager_id_2_tab_2,
    #                     gameweek_tab_2,
    #                     search_button_tab_2,
    #                 ) = mini_league_search_bar()
    #             with ui.tab_panel(top_5_search_tab):
    #                 ui.label("pass")
    #                 # (
    #                 #     manager_id_1_tab_3,
    #                 #     manager_id_2_tab_3,
    #                 #     gameweek_tab_3,
    #                 #     search_button_tab_3,
    #                 # ) = await top_50_search()

    # complete_div = ui.element("div").classes("w-screen h-auto")

    # search(
    #     full_div,
    #     manager_id_1_tab_1,
    #     manager_id_2_tab_1,
    #     gameweek_tab_1,
    #     search_button_tab_1,
    #     complete_div,
    # )

    # search(
    #     full_div,
    #     manager_id_1_tab_2,
    #     manager_id_2_tab_2,
    #     gameweek_tab_2,
    #     search_button_tab_2,
    #     complete_div,
    # )

    # search(
    #     full_div,
    #     manager_id_1_tab_3,
    #     manager_id_2_tab_3,
    #     gameweek_tab_3,
    #     search_button_tab_3,
    #     complete_div,
    # )
