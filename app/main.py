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
        padding:0;
        margin:0;
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

    .gw_select_class.q-field--outlined .q-field__control {
    padding: 0 2px;
    }

    .gw_select_class.q-field__after, .q-field__append {
    padding-left: 4px;
    }
    .manager_select_class.q-field--outlined .q-field__control {
    border-top-left-radius:0px;
    border-bottom-left-radius:0px;
    border-top-right-radius:0px;
    border-bottom-right-radius:0px;
    }

    .q-field__label {
            font-size:14px
    }

    @media only screen and (min-width: 40em) {
        .q-field__label {
            font-size:16px
        }
        .gw_select_class.q-field--outlined .q-field__control {
            padding: 0 8px;
            }

        .gw_select_class.q-field__after, .q-field__append {
            padding-left: 12px;
        }
    }

    .q-toggle__inner--truthy .q-toggle__thumb {
    left: 0.85em;
    }
    .q-toggle__inner {
    width: 1.6em;
    }
    .q-toggle__track {
    height: 0.5em;
    border-radius: 0.4em;
    }
    .q-toggle__thumb {
    top: 0.375em;
    left: 0.35em;
    width: 0.4em;
    height: 0.4em;
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
