from common_format import display
import page_creation
import asyncio
from nicegui import ui, Client, globals
from fastapi import FastAPI
from router import Router

# app = FastAPI()

# page_creation.create(app)


@ui.page("/")  # normal index page (e.g. the entry point of the app)
@ui.page(
    "/{_:path}"
)  # all other pages will be handled by the router but must be registered
# to also show the SPA index page
def main(client: Client):
    client.content.classes("p-0 m-0")
    router = Router()

    @router.add("/")
    def home():
        page_creation.home_page()

    @router.add("/search_manager_id")
    def manager_id():
        page_creation.by_manager_id_page()

    @router.add("/search_mini_league")
    def mini_league():
        page_creation.by_mini_league_page()

    @router.add("/search_top")
    def top_managers():
        page_creation.by_top_5_page()

    display(
        [
            (home, "Home"),
            (manager_id, "Manager ID"),
            (mini_league, "Mini League"),
            (top_managers, "Top 5"),
        ],
        router,
    )
    # this places the content which should be displayed
    router.frame().classes("w-full")


ui.run()
