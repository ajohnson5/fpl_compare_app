from common_format import display
import home
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
    ui.add_head_html(
        """<style>
    body {
        max-width: 100%;
        overflow-x:hidden;
    }
    .input_class.q-field--outlined .q-field__control {
    border-top-left-radius:9999px;
    border-bottom-left-radius:9999px;
    border-top-right-radius:0px;
    border-bottom-right-radius:0px;
    }
    .gw_select_class.q-field--outlined .q-field__control {
    border-top-left-radius:0px;
    border-bottom-left-radius:0px;
    border-top-right-radius:9999px;
    border-bottom-right-radius:9999px;
    }
    </style>
    """
    )

    client.content.classes("p-0 m-0")
    router = Router()

    # @router.add("/")
    # def home_page():
    #     index.show_page()

    @router.add("/")
    async def home_page():
        await home.show_page()

    display(
        [
            (home_page, "Home"),
        ],
        router,
    )
    # this places the content which should be displayed
    router.frame().classes("w-full")


ui.run()
