from nicegui import ui


def combined_search_without_gw(input_class: str):
    with ui.element("div").classes(
        "flex flex-row gap-x-0 w-full content-center justify-center align-middle "
        "items-center h-full"
    ) as input_container:
        # Checkbox to indicate if the manager id or league id input is in use
        with ui.element("div").classes(
            "w-[40px] flex flex-row justify-start align-middle items-center"
        ):
            search_toggle = ui.checkbox().classes(input_class)

        # Container for manager and league id inputs
        with ui.element("div").classes("grow relative h-[58px] mr-8"):
            # Manager Id input on top layer
            manager_id_input = (
                ui.input("Manager ID")
                .classes("input_class")
                .classes(input_class)
                .classes("absolute top-0 left-0 w-full z-0")
                .props('clearable outlined inputmode="search" mask="##########"')
            )

            with manager_id_input.add_slot("prepend"):
                ui.icon("person")

            #
            with ui.element("div").classes(
                "absolute top-0 left-0 w-full z-10 overflow-hidden flex flex-row"
            ):
                # League Id input on second layer
                league_id_input = (
                    ui.input("League ID")
                    .classes("input_class")
                    .classes(input_class)
                    .classes("h-[55px]")
                    .props(
                        'outlined inputmode="search" mask="##########" bg-color="white"'
                    )
                ).style(
                    "width:100%;transition: 0.5s cubic-bezier(0.4, 0, 0.2, 1);"
                    "-webkit-transition: 0.5s cubic-bezier(0.4, 0, 0.2, 1); "
                    "-moz-transition: 0.5s cubic-bezier(0.4, 0, 0.2, 1); "
                    "-o-transition: 0.5s cubic-bezier(0.4, 0, 0.2, 1); "
                )

                with league_id_input.add_slot("prepend"):
                    ui.icon("leaderboard")

                # Manager select on second layer but has 0 initial width
                # Expands on successful league id input
                manager_select = (
                    ui.select(
                        options=[],
                        label="Manager",
                        with_input=False,
                    )
                    .classes("manager_select_class")
                    .classes(input_class)
                    .classes("h-full")
                    .props('outlined bg-color="white" behavior="menu"')
                    .style(
                        "width:0;transition:width 0.5s cubic-bezier(0.4, 0, 0.2, 1);"
                        "-webkit-transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1); "
                        "-moz-transition:width 0.5s cubic-bezier(0.4, 0, 0.2, 1); "
                        "-o-transition:width 0.5s cubic-bezier(0.4, 0, 0.2, 1); "
                    )
                )
    return (
        search_toggle,
        manager_id_input,
        league_id_input,
        manager_select,
        input_container,
    )


def dual_search():
    # Create combined searches for manager's 1 and 2
    with ui.element("div").classes("grid grid-cols-1 grid-rows-2 gap-y-0"):
        (
            search_toggle_1,
            manager_id_input_1,
            league_id_input_1,
            manager_select_1,
            manager_1_container,
        ) = combined_search_without_gw("manager_1_input_class")

        (
            search_toggle_2,
            manager_id_input_2,
            league_id_input_2,
            manager_select_2,
            manager_2_container,
        ) = combined_search_without_gw("manager_2_input_class")

    manager_1_container.classes("col-span-1 row-span-1")
    manager_2_container.classes("col-span-1 row-span-1")

    manager_id_input_1.props('color="light-blue-7"')
    manager_id_input_2.props('color="red-7"')

    league_id_input_1.props('color="light-blue-7"')
    league_id_input_2.props('color="red-7"')

    manager_select_1.props('color="light-blue-7"')
    manager_select_2.props('color="red-7"')

    return (
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
    )
