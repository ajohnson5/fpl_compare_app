from common_format import display
import compare
import index
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
async def main(client: Client):
    client.content.classes("p-0 m-0")
    router = Router()

    @router.add("/")
    def home_page():
        index.show_page()

    @router.add("/compare")
    async def compare_page():
        await compare.show_page()

    display(
        [
            (home_page, "Home"),
            (compare_page, "Compare"),
        ],
        router,
    )
    # this places the content which should be displayed
    router.frame().classes("w-full")


ui.run()
