import common_format
import index
import asyncio

import manager_id
import mini_league
import top

from fastapi import FastAPI

from nicegui import ui, app


def home_page():
    index.show_page()


def by_manager_id_page():
    manager_id.show_page()


def by_mini_league_page():
    mini_league.show_page()


def by_top_5_page():
    top.show_page()


def create(fastapi_app: FastAPI) -> None:
    home_page()
    by_manager_id_page()
    by_manager_id_page()
    by_manager_id_page()

    ui.run_with(
        fastapi_app,
    )
