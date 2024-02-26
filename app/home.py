from nicegui import ui
import asyncio
from common_format import display
from fpl_api import get_manager_name, get_league_managers
from compare_squads import compare_squads
from layout_components import (
    manager_summary_layout,
    pitch_layout,
    bench_layout,
    transfer_layout,
    player_icon_key,
    fixture_layout,
    dual_search,
)

# Latest completed gameweek
CURRENT_GAMEWEEK = 25


async def show_page():
    # Dictionary to store previous manager_ids, league_ids
    # (Only configured to remember same session)
    previous_ids = {"manager_ids": {}, "league_ids": {}}

    # Chip dictionary to store "active" managers (name and id) and gameweek
    chip_state = {
        "chip_1": None,
        "chip_2": None,
        "chip_1_id": None,
        "chip_2_id": None,
        "chip_1_gw": CURRENT_GAMEWEEK,
        "chip_2_gw": CURRENT_GAMEWEEK,
    }

    # Func to set the gameweek
    def set_gameweek(gameweek, manager_num, gameweek_button):
        if manager_num == 1:
            gameweek_button.set_text(str(gameweek))
            chip_state["chip_1_gw"] = gameweek
        else:
            chip_state["chip_2_gw"] = gameweek

    # Func to search for a league with league id and return the managers in the league
    async def search_league(league_id, league_input, manager_select):
        # Check league id input is valid
        if not league_id:
            with league_input.add_slot("prepend"):
                with ui.icon("error", color="red-500"):
                    ui.tooltip("Please enter a League ID").classes("bg-red-500")
                league_input.update()
            return

        # Clear manager select and get the managers in a league
        manager_select.clear()
        manager_select.set_value(value=None)
        managers = await get_league_managers(int(league_id))

        # If the league exists and contains managers show the manager select input
        if managers:
            with league_input.add_slot("prepend"):
                ui.icon("check_circle", color="green-500")
            manager_select.style("width:65%;")
            league_input.style("width:35%;")
            if league_input == league_id_input_1:
                league_input.classes("update_league_id_input_radius")
                manager_select.classes("update_manager_select_radius")
            previous_ids["league_ids"][league_id] = "A league"
            update_league_id_store()
            league_input.update()
        # Otherwise notify that the league is invalid
        else:
            with league_input.add_slot("prepend"):
                with ui.icon("error", color="red-500"):
                    ui.tooltip("Invalid League ID").classes("bg-red-500")
            league_input.update()
            return

        manager_select.options = managers
        manager_select.update()

    # Refreshable func to list all previosuly entered manager ids in nav bar
    @ui.refreshable
    def update_id_store():
        manager_id_store.clear()
        with manager_id_store:
            for id, name in previous_ids["manager_ids"].items():
                with ui.element("div").classes(
                    "w-full border-2 rounded-xl border-stone-600 p-2 grid grid-cols-5 "
                    "mb-4"
                ):
                    with ui.element("div").classes(
                        "flex flex-row items-center col-span-4"
                    ):
                        ui.label(f"ID: {id}").classes(
                            "w-full text-left font-bold text-md"
                        )
                        ui.label(f"Name: {name}").classes(
                            "w-full text-left font-bold text-md"
                        )

                    with ui.element("div").classes("col-span-1"):
                        ui.button(
                            "1",
                            on_click=lambda id=id, name=name: set_chip_from_store(
                                id, name, 1
                            ),
                        ).props("push ").classes("mb-1").classes("set_manager_1_button")
                        ui.button(
                            "2",
                            on_click=lambda id=id, name=name: set_chip_from_store(
                                id, name, 2
                            ),
                        ).props("push ").classes("set_manager_2_button")

    # Refreshable func to list all previosuly entered league ids in nav bar
    @ui.refreshable
    def update_league_id_store():
        league_id_store.clear()
        with league_id_store:
            for league_id, league_name in previous_ids["league_ids"].items():
                with ui.element("div").classes(
                    "w-full border-2 rounded-xl border-stone-600 p-2 grid grid-cols-5 "
                    "mb-4"
                ):
                    with ui.element("div").classes(
                        "flex flex-row items-center col-span-4"
                    ):
                        ui.label(f"ID: {league_id}").classes(
                            "w-full text-left font-bold text-md"
                        )
                        ui.label(f"Name: {league_name}").classes(
                            "w-full text-left font-bold text-md"
                        )

                    with ui.element("div").classes("col-span-1"):
                        ui.button(
                            "1",
                            on_click=lambda league_id=league_id: set_league_from_store(
                                league_id, league_id_input_1, manager_select_1
                            ),
                        ).props("push ").classes("mb-1").classes("set_manager_1_button")
                        ui.button(
                            "2",
                            on_click=lambda league_id=league_id: set_league_from_store(
                                league_id, league_id_input_2, manager_select_2
                            ),
                        ).props("push ").classes("set_manager_2_button")

    # Add/update chip dictionary with manager name when a manager id is input
    def add_chip(manager_id, manager_num, manager_input):
        if manager_id and manager_num:
            if manager_num == 1:
                manager_name = get_manager_name(manager_id)
                if manager_name:
                    chip_state["chip_1_id"] = int(manager_id)
                    chip_state["chip_1"] = manager_name
                    manager_input.set_value("")
                    previous_ids["manager_ids"][manager_id] = manager_name
                    update_id_store()
                else:
                    ui.notify("Manager does not exist", closeBtn="OK")
            else:
                manager_name = get_manager_name(manager_id)
                if manager_name:
                    chip_state["chip_2_id"] = int(manager_id)
                    chip_state["chip_2"] = manager_name
                    manager_input.set_value("")
                    previous_ids["manager_ids"][manager_id] = manager_name
                    update_id_store()
                else:
                    ui.notify("Manager does not exist", closeBtn="OK")
        else:
            pass

    # Func to set the chip (manager_id, manager_name) from the manager_id store in nav
    def set_chip_from_store(manager_id, manager_name, manager_num):
        if manager_num == 1:
            chip_state["chip_1_id"] = int(manager_id)
            chip_state["chip_1"] = manager_name
        else:
            chip_state["chip_2_id"] = int(manager_id)
            chip_state["chip_2"] = manager_name

    # Func to set the league id and managers select from the league_id store in nav_bar
    async def set_league_from_store(league_id, league_input, manager_select):
        with league_input.add_slot("prepend"):
            ui.icon("check_circle", color="green-500")
        manager_select.style("width:65%;")
        league_input.style("width:35%;")
        if league_input == league_id_input_1:
            league_input.classes("update_league_id_input_radius")
            manager_select.classes("update_manager_select_radius")
        league_input.update()

        league_input.set_value(league_id)
        managers = await get_league_managers(int(league_id))

        manager_select.options = managers
        manager_select.update()

    # Func to generate squad comparison and display the comparison
    async def load_display():
        if chip_state["chip_1"] and chip_state["chip_2"]:
            await compare_squads(
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
                fixture_1_display,
                fixture_2_display,
            )
        else:
            ui.notify("Please enter 2 manager IDs", closeBtn="OK")

    # Func to return to search page from comparison page
    async def return_to_landing():
        landing_div.set_visibility(True)
        display_div.set_visibility(False)

    ##########################################################################
    ##########################################################################
    ######################## Start of Search Page ############################
    ##########################################################################
    ##########################################################################

    # Navigation bar for storing previously used managers
    nav_bar, manager_id_store, league_id_store = display()

    with ui.element("div").classes(
        "w-screen h-screen flex flex-row justify-center align-middle bg-stone-50"
    ):
        with ui.element("div").classes(
            "w-screen flex flex-row justify-center align-middle items-center"
        ) as landing_div:
            with ui.element("div").classes(
                "grid grid-cols-12 grid-rows-7 w-[340px] h-[300px]"
            ) as manager_1_container:
                # Chip 1 for manager 1
                with ui.element("div").classes(
                    "flex flex-row justify-center items-center col-span-12 "
                    "row-span-1 h-[80px]"
                ):
                    with ui.element("div").classes(
                        "flex flex-row justify-center items-center rounded-full "
                        "bg-gradient-to-r from-sky-500 via-sky-300 to-cyan-400 "
                        "gap-x-1 p-1"
                    ) as chip_container_1:
                        # Manager 1 label
                        manager_name_1 = ui.label("").classes(
                            "font-extrabold text-2xl text-sky-500 px-4 py-2 "
                            "rounded-l-full bg-stone-100"
                        )
                        # Gameweek select for manager 1
                        with ui.button(CURRENT_GAMEWEEK, color="stone-100").props(
                            ""
                        ).classes("w-[50px]").classes("gameweek_button").classes(
                            "gameweek_1"
                        ) as gameweek_1:
                            with ui.menu().classes("w-[180px] grid grid-cols-5"):
                                for i in range(1, CURRENT_GAMEWEEK + 1):
                                    ui.menu_item(
                                        i, lambda i=i: set_gameweek(i, 1, gameweek_1)
                                    ).classes("col-span-1")

                # Dual Search for manager 1 and 2
                with ui.element("div").classes(
                    "grid grid-cols-12 grid-rows-2 justify-center items-center "
                    "align-middle col-span-12 row-span-2 py-1"
                ):
                    with ui.element("div").classes("col-span-12 row-span-2"):
                        (
                            search_toggle_1,
                            manager_id_input_1,
                            league_id_input_1,
                            manager_select_1,
                            manager_1_container,
                            search_toggle_2,
                            manager_id_input_2,
                            league_id_input_2,
                            manager_select_2,
                            manager_2_container,
                        ) = dual_search()

                # Chip 2 for manager 2
                with ui.element("div").classes(
                    "flex flex-row justify-center items-center col-span-12 "
                    "row-span-1 h-[80px]"
                ):
                    with ui.element("div").classes(
                        "flex flex-row justify-center items-center rounded-full "
                        "bg-gradient-to-r from-red-500 via-red-400 to-rose-400 "
                        "gap-x-1 p-1"
                    ) as chip_container_2:
                        # Manager 2 label
                        manager_name_2 = ui.label("").classes(
                            "font-extrabold text-2xl text-red-500 px-4 py-2 "
                            "rounded-l-full bg-stone-100"
                        )
                        # Gameweek select for manager 2
                        with ui.button(CURRENT_GAMEWEEK, color="stone-100").props(
                            ""
                        ).classes("w-[50px]").classes("gameweek_button").classes(
                            "gameweek_2"
                        ) as gameweek_2:
                            with ui.menu().classes("w-[180px] grid grid-cols-5"):
                                for i in range(1, CURRENT_GAMEWEEK + 1):
                                    ui.menu_item(
                                        i, lambda i=i: set_gameweek(i, 2, gameweek_2)
                                    ).classes("col-span-1")

                    # League ID and manager select visibility bindings for Manager 1&2
                    league_id_input_1.bind_visibility_from(search_toggle_1, "value")
                    manager_select_1.bind_visibility_from(search_toggle_1, "value")

                    league_id_input_2.bind_visibility_from(search_toggle_2, "value")
                    manager_select_2.bind_visibility_from(search_toggle_2, "value")

                    # Label bindings for Manager 1
                    chip_container_1.bind_visibility_from(chip_state, "chip_1")
                    manager_name_1.bind_text_from(chip_state, "chip_1")
                    gameweek_1.bind_text_from(chip_state, "chip_1_gw")

                    # Label bindings for Manager 2
                    chip_container_2.bind_visibility_from(chip_state, "chip_2")
                    manager_name_2.bind_text_from(chip_state, "chip_2")
                    gameweek_2.bind_text_from(chip_state, "chip_2_gw")

                    # Manager 1 Search / Inputs
                    league_id_input_1.on(
                        "keydown.enter",
                        lambda: search_league(
                            league_id_input_1.value, league_id_input_1, manager_select_1
                        ),
                    )
                    manager_id_input_1.on(
                        "keydown.enter",
                        lambda x: add_chip(
                            manager_id_input_1.value, 1, manager_id_input_1
                        ),
                    )
                    manager_select_1.on(
                        "update:model-value",
                        lambda x: add_chip(manager_select_1.value, 1, manager_select_1),
                    )

                    # Manager 1 Search / Inputs
                    league_id_input_2.on(
                        "keydown.enter",
                        lambda: search_league(
                            league_id_input_2.value, league_id_input_2, manager_select_2
                        ),
                    )

                    manager_id_input_2.on(
                        "keydown.enter",
                        lambda x: add_chip(
                            manager_id_input_2.value, 2, manager_id_input_2
                        ),
                    )

                    manager_select_2.on(
                        "update:model-value",
                        lambda x: add_chip(manager_select_2.value, 2, manager_select_2),
                    )

        # Create compare button to compare the two managers squads
        compare_button = (
            ui.button(icon="search")
            .props("round flat size=20px")
            .classes("h-[40px] absolute bottom-4 right-4")
        )
        compare_button.on("click", load_display, throttle=1.0)

        ##########################################################################
        ##########################################################################
        ####################### Start of Display Page ############################
        ##########################################################################
        ##########################################################################

        with ui.element("div").classes(
            "flex flex-row justify-center content-center w-full min-h-screen "
            "bg-stone-50 relative bottom-bottom-1"
        ) as display_div:
            # Create page header with return button to switch back to the search page
            with ui.element("div").classes(
                "flex flex-row w-full h-auto mb-6 mt-[110px] z-0 justify-between "
                "items-center align-middle"
            ):
                ui.button(
                    text="back",
                    icon="arrow_back_ios",
                    on_click=lambda x: return_to_landing(),
                ).props("flat outline rounded size=10px color=grey-10").classes(
                    "w-[60px] mt-4"
                ).classes(
                    "return_button_class"
                )

                ui.label("Squads.").classes(
                    "text-6xl sm:text-7xl text-zinc-900 font-sans font-bold h-auto "
                    "w-auto text-center align-middle"
                )

                ui.label().classes("w-[60px]")

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

            # Create upcoming fixtures layout

            fixture_1_display, fixture_2_display = fixture_layout()

        display_div.set_visibility(False)
