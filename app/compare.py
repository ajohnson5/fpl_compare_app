#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Callable, List
import requests
from nicegui import ui, Tailwind, app
import pandas as pd
from typing import Self
import asyncio


from squad_display import show_squad
from search import (
    manager_id_search,
    top_search,
    search,
    manager_id_search_bar,
    top_50_search,
    mini_league_search_bar,
)

manager_id_1, manager_id_2, gameweek, search_button = manager_id_search_bar()


async def show_page():
    with ui.element("div").classes(
        "flex flex-row justify-center items-center content-center"
    ) as full_div:
        with ui.element("div").classes(
            "w-full max-w-[500px] border-2 border-slate-300 drop-shadow-xl mx-2"
        ):
            with ui.tabs() as tabs:
                manager_id_search_tab = ui.tab("Manager ID")
                mini_league_search_tab = ui.tab("Mini League")
                top_5_search_tab = ui.tab("Top 5")
            ui.separator()
            with ui.tab_panels(
                tabs, value=manager_id_search_tab, animated=False
            ).classes("w-full h-[200px]"):
                with ui.tab_panel(manager_id_search_tab):
                    (
                        manager_id_1_tab_1,
                        manager_id_2_tab_1,
                        gameweek_tab_1,
                        search_button_tab_1,
                    ) = manager_id_search_bar()
                with ui.tab_panel(mini_league_search_tab):
                    (
                        manager_id_1_tab_2,
                        manager_id_2_tab_2,
                        gameweek_tab_2,
                        search_button_tab_2,
                    ) = mini_league_search_bar()
                with ui.tab_panel(top_5_search_tab):
                    (
                        manager_id_1_tab_3,
                        manager_id_2_tab_3,
                        gameweek_tab_3,
                        search_button_tab_3,
                    ) = await top_50_search()

    error_message = ui.element("div")

    complete_div = ui.element("div").classes("w-full h-auto")

    search(
        full_div,
        manager_id_1_tab_1,
        manager_id_2_tab_1,
        gameweek_tab_1,
        search_button_tab_1,
        error_message,
        complete_div,
    )

    search(
        full_div,
        manager_id_1_tab_2,
        manager_id_2_tab_2,
        gameweek_tab_2,
        search_button_tab_2,
        error_message,
        complete_div,
    )

    search(
        full_div,
        manager_id_1_tab_3,
        manager_id_2_tab_3,
        gameweek_tab_3,
        search_button_tab_3,
        error_message,
        complete_div,
    )
