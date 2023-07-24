from nicegui import ui
import asyncio

from fpl_api import get_manager_name, get_league_managers
from generate_squad import generate_squad
from layout_components import (
    combined_search,
    manager_chip,
    manager_summary_layout,
    pitch_layout,
    bench_layout,
    transfer_layout,
    player_icon_key,
    compare_button_func,
)


async def show_page():
    ##########################################################################
    ##########################################################################
    ####################### UI / Search Functions  ###########################
    ##########################################################################
    ##########################################################################

    chip_state = {
        "chip_1": None,
        "chip_2": None,
        "chip_1_id": None,
        "chip_2_id": None,
        "chip_1_gw": None,
        "chip_2_gw": None,
    }

    async def search_league(league_id):
        if not league_id:
            with league_id_input.add_slot("prepend"):
                with ui.icon("error", color="red-500"):
                    ui.tooltip("Please enter a League ID").classes("bg-red-500")
                league_id_input.update()
            return

        manager_select.clear()

        manager_select.set_value(value=None)

        managers = await get_league_managers(int(league_id))

        managers = {
            12313: "Ujedinjeni Urci",
            2131: "Badger Oblong Quasi",
            3763: "Bad Team On Paper",
        }

        if managers:
            with league_id_input.add_slot("prepend"):
                ui.icon("check_circle", color="green-500")
                manager_select.style("width:50%;")
                league_id_input.style("width:50%;")
                league_id_input.update()
        else:
            with league_id_input.add_slot("prepend"):
                with ui.icon("error", color="red-500"):
                    ui.tooltip("Invalid League ID").classes("bg-red-500")
                league_id_input.update()
            return

        manager_select.options = managers
        manager_select.update()

    def add_chip(manager_id, gameweek_select):
        if manager_id and gameweek_select:
            if not chip_state["chip_1"]:
                manager_name = get_manager_name(manager_id)
                if manager_name:
                    chip_state["chip_1_id"] = int(manager_id)
                    chip_state["chip_1"] = manager_name
                    chip_state["chip_1_gw"] = gameweek_select
                    chip_1.style("visibility:visible")
                    manager_id_input.set_value("")

                else:
                    ui.notify("Manager does not exist", closeBtn="OK")
            elif not chip_state["chip_2"]:
                manager_name = get_manager_name(manager_id)
                if manager_name:
                    chip_state["chip_2_id"] = int(manager_id)
                    chip_state["chip_2"] = manager_name
                    chip_state["chip_2_gw"] = gameweek_select
                    chip_2.style("visibility:visible")
                    manager_id_input.set_value("")
                else:
                    ui.notify("Manager does not exist", closeBtn="OK")
        else:
            pass

    def delete_chip(chip):
        if chip == chip_1:
            chip_state["chip_1"] = None
        else:
            chip_state["chip_2"] = None

        chip.style("visibility:hidden")

    async def load_display():
        if chip_state["chip_1"] and chip_state["chip_2"]:
            await generate_squad(
                chip_state,
                display_div,
                landing_div,
                manager_1_display,
                manager_2_display,
                squad_1_display,
                squad_2_display,
                bench_1_display,
                bench_2_display,
                transfer_1_display,
                transfer_2_display,
            )
        else:
            ui.notify("Please enter 2 manager IDs", closeBtn="OK")

    ##########################################################################
    ##########################################################################
    ########################## Start of Web Page  ############################
    ##########################################################################
    ##########################################################################

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
                compare_button = compare_button_func()

                ui.label("Squads.").classes(
                    "text-5xl sm:text-6xl text-stone-100 font-sans font-bold h-auto "
                    "w-auto text-center align-middle mb-3"
                )

            search_toggle = (
                ui.switch()
                .classes("absolute top-[85vh] right-[5px]")
                .props('size="70px" checked-icon="leaderboard" unchecked-icon="person"')
            )

            with ui.element("div").classes(
                "h-1/4 w-full flex flex-row content-start justify-center relative mx-2"
            ):
                (
                    manager_id_input,
                    league_id_input,
                    manager_select,
                    gameweek_select,
                ) = combined_search()

                with ui.element("div").classes(
                    "w-full flex flex-row justify-center content-start gap-x-4 gap-y-6 "
                    "pt-6"
                ):
                    (
                        chip_1,
                        manager_name_1,
                        delete_chip_1,
                        gw_chip_label_1,
                    ) = manager_chip(True)
                    (
                        chip_2,
                        manager_name_2,
                        delete_chip_2,
                        gw_chip_label_2,
                    ) = manager_chip(False)

            ui.element("div").classes(
                "h-1/6 w-full flex flex-row content-start justify-center"
            )

            ##########################################################################
            ##########################################################################
            ########################## Bindings / Search  ############################
            ##########################################################################
            ##########################################################################

            # League Search visibility toggle
            league_id_input.bind_visibility_from(search_toggle, "value")
            manager_select.bind_visibility_from(search_toggle, "value")

            # Searches / Inputs
            league_id_input.on(
                "keydown.enter", lambda: search_league(league_id_input.value)
            )

            manager_id_input.on(
                "keydown.enter",
                lambda x: add_chip(manager_id_input.value, gameweek_select.value),
            )

            manager_select.on(
                "update:model-value",
                lambda x: add_chip(manager_select.value, gameweek_select.value),
            )

            # Chips - Update chip labels
            gw_chip_label_1.bind_text_from(chip_state, "chip_1_gw")
            gw_chip_label_2.bind_text_from(chip_state, "chip_2_gw")
            manager_name_1.bind_text_from(chip_state, "chip_1")
            manager_name_2.bind_text_from(chip_state, "chip_2")

            # Delete chip values - Set visibility to false
            delete_chip_1.on("click", lambda x: delete_chip(chip_1))
            delete_chip_2.on("click", lambda x: delete_chip(chip_2))

            # Load Display page when Compare button pressed
            compare_button.on("click", load_display)

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
                "border-top: 50px solid #e0f2fe;border-right:80px solid transparent;"
                "background-color: transparent"
            )

            ui.label("Squads.").classes(
                "text-6xl sm:text-7xl text-zinc-900 font-sans font-bold h-auto "
                "w-auto text-center align-middle mb-6 mt-[60px]"
            )

            # Create manager summary sections
            manager_1_display, manager_2_display = manager_summary_layout()

            # Create player icon key - captain, automatic subs, etc
            player_icon_key()

            # Create pitch and general structure for manager's starting XI
            squad_1_display, squad_2_display = pitch_layout()

            # Create bench layout for both managers
            bench_1_display, bench_2_display = bench_layout()

            # Create transfer layout for transfers managers' made
            transfer_1_display, transfer_2_display = transfer_layout()

        display_div.set_visibility(False)
