import common_format
import index
import asyncio

import manager_id
import mini_league
import top

from fastapi import FastAPI

from nicegui import ui, app


@ui.page("/")
def home_page():
    with common_format.display():
        index.show_page()


@ui.page("/search_manager_id")
def by_manager_id_page():
    with common_format.display():
        manager_id.show_page()


@ui.page("/search_mini_league")
def by_mini_league_page():
    with common_format.display():
        mini_league.show_page()


@ui.page("/search_top")
def by_top_5_page():
    with common_format.display():
        top.show_page()


def create(fastapi_app: FastAPI) -> None:
    home_page()
    by_manager_id_page()
    by_manager_id_page()
    by_manager_id_page()

    ui.run_with(
        fastapi_app,
    )
