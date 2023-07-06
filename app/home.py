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


async def show_page():
    with ui.element("div").classes(
        (
            "flex flex-row justify-center items-center content-center h-screen "
            "w-screen bg-gradient-to-b from-blue-400 via-blue-300 to-white gap-y-14"
        )
    ):
        ui.label("Compare Squads.").classes(
            "text-4xl sm:text-5xl text-white font-sans font-bold w-full text-center"
        )

        input_1, gw_select_1 = input_with_select()

        input_1.classes("w-2/3 max-w-[300px]")
        gw_select_1.classes("w-1/3 max-w-[100px]")

        ui.button("Compare", icon="change_circle").classes("w-[200px] h-[60px]").props(
            'rounded text-color="black" size="lg" color="white"'
        )

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
