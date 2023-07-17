from nicegui import ui
import asyncio


async def show_page():
    await asyncio.sleep(0)
    with ui.element("div").classes(
        "flex flex-row justify-center items-center content-center h-screen "
        "w-screen bg-stone-100 "
    ):
        ui.label("About.").classes(
            "text-5xl sm:text-6xl text-slate-900 font-sans font-bold h-auto "
            "w-auto text-center align-middle"
        )
