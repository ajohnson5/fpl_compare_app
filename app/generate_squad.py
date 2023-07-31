from nicegui import ui
import asyncio
from layout_components import create_button


async def show_page():
    with ui.element("div").classes("flex flex-row"):
        with ui.element("div").classes(
            "flex flex-row justify-center items-center content-center h-screen "
            "w-screen bg-transparent"
        ):
            ui.element("div").classes("h-1/5 w-full")

            with ui.element("div").classes(
                "h-1/4 w-full flex flex-row justify-center content-end items-center "
                "pb-6 gap-x-2"
            ):
                create_button("Generate")

                ui.label("Squads.").classes(
                    "text-5xl sm:text-6xl text-stone-100 font-sans font-bold h-auto "
                    "w-auto text-center align-middle mb-3"
                )

            ui.element("div").classes(
                "h-1/4 w-full flex flex-row content-start justify-center"
            )

            ui.element("div").classes(
                "h-1/6 w-full flex flex-row content-start justify-center"
            )
