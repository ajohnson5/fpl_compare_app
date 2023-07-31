from nicegui import ui
import asyncio
from layout_components import create_button, generate_squad_pitch_layout, squad_summary

from squad import Squad, RandomSquadGenerator

generator = RandomSquadGenerator()


async def generate_squad(
    loading_div, display_div, squad_display, squad_summary_display
):
    with loading_div:
        with ui.element("div") as loading_clearable_div:
            with ui.element("div").classes(
                (
                    "flex flex-row w-full h-full fixed top-0 left-0 bg-stone-200/50 "
                    "items-center justify-center content-center backdrop-blur-sm z-50"
                )
            ):
                ui.spinner(size="xl", thickness=10.0)
    await asyncio.sleep(1.0)

    generator.create_random_squad()

    with squad_summary_display:
        squad_summary_display.clear()
        generator.squad.create_squad_summary_display()

    with squad_display:
        squad_display.clear()

        generator.squad.create_team_display()

    loading_clearable_div.clear()
    display_div.set_visibility(True)


async def show_page():
    with ui.element("div").classes("flex flex-row"):
        with ui.element("div").classes(
            "flex flex-row justify-center items-center content-center h-screen "
            "w-screen bg-transparent"
        ) as landing_div:
            ui.element("div").classes("h-1/5 w-full")

            with ui.element("div").classes(
                "h-1/4 w-full flex flex-row justify-center content-end items-center "
                "pb-6 gap-x-2"
            ):
                generate_button = create_button("Generate")

                ui.label("Squads.").classes(
                    "text-5xl sm:text-6xl text-stone-100 font-sans font-bold h-auto "
                    "w-auto text-center align-middle mb-3"
                )

            with ui.element("div").classes(
                "h-1/4 w-full flex flex-row content-start justify-center"
            ):
                ui.toggle(
                    {
                        1: "Actually Random",
                        2: "A Real Team Please",
                    },
                    value=1,
                ).props(
                    'rounded color="white" text-color="black" spread padding="12px"'
                ).classes(
                    "w-full max-w-[400px] mx-2"
                )
            ui.element("div").classes(
                "h-1/6 w-full flex flex-row content-start justify-center"
            )

        ##########################################################################
        ##########################################################################
        ####################### Start of Display Page ############################
        ##########################################################################
        ##########################################################################

        with ui.element("div").classes(
            "flex flex-row justify-center content-center w-full min-h-screen "
            "bg-white relative bottom-bottom-1 border-sky-400"
        ) as display_div:
            ui.label().classes("w-[calc(50vw_+_40px)] absolute top-0 left-0").style(
                "border-top: 50px solid #cffafe;border-right:80px solid transparent;"
                "background-color: transparent"
            )

            ui.label("Squads.").classes(
                "text-6xl sm:text-7xl text-zinc-900 font-sans font-bold h-auto "
                "w-full  text-center align-middle mb-6 mt-[60px]"
            )

            squad_summary_display = squad_summary()
            squad_display = generate_squad_pitch_layout()

        display_div.set_visibility(False)

        ##########################################################################
        ##########################################################################
        ########################## Bindings / Search  ############################
        ##########################################################################
        ##########################################################################

        # Load Display page when Compare button pressed
        generate_button.on(
            "click",
            lambda x: generate_squad(
                landing_div, display_div, squad_display, squad_summary_display
            ),
            throttle=1.0,
        )
