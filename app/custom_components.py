from nicegui import ui


def input_with_select():
    with ui.element("div").classes(
        "flex flex-row gap-x-0 w-full content-center justify-center w-full "
        "min-w-[300px] max-w-[400px]"
    ):
        input = (
            ui.input("Manager ID")
            .classes("input_class")
            .props(
                (
                    'clearable outlined mask="############" inputmode="numeric" '
                    'bg-color="white"'
                )
            )
        )

        with input.add_slot("prepend"):
            ui.icon("search")

        select = (
            ui.select([1, 2, 3], value=1, label="GW")
            .classes("gw_select_class")
            .props('outlined bg-color="white" behavior="menu"')
        )

    return input, select


def league_search():
    with ui.element("div").classes(
        "flex flex-row gap-x-0 w-full content-center justify-center w-full "
        "max-w-[400px]"
    ) as league_search_div:
        input = (
            ui.input("League ID")
            .classes("input_class")
            .props(
                ('outlined mask="############" inputmode="numeric" bg-color="white"')
            )
        )

        with input.add_slot("prepend"):
            ui.icon("leaderboard")

        select = (
            ui.select(
                options=[],
                label="Manager",
                with_input=True,
            )
            .classes("manager_select_class")
            .props('outlined bg-color="white" behavior="menu"')
        )

        gw_select = (
            ui.select([1, 2, 3], value=1, label="GW")
            .classes("gw_select_class")
            .props('outlined bg-color="white" behavior="menu"')
        )

    return input, select, gw_select, league_search_div


def combined_search():
    with ui.element("div").classes(
        "flex flex-row gap-x-0 w-full content-center justify-center w-full "
        "min-w-[300px] max-w-[400px]"
    ):
        with ui.element("div").classes("grow relative h-auto"):
            manager_id_input = (
                ui.input("Manager ID")
                .classes("input_class")
                .classes("absolute top-0 left-0 w-full z-0")
                .props(
                    (
                        'clearable outlined mask="############" inputmode="numeric" '
                        'bg-color="white"'
                    )
                )
            )

            with manager_id_input.add_slot("prepend"):
                ui.icon("search")

            with ui.element("div").classes(
                "absolute top-0 left-0 w-full z-10 flex flex-row overflow-hidden"
            ):
                league_id_input = (
                    ui.input("League ID")
                    .classes("input_class")
                    .classes("w-full h-full")
                    .props(
                        'outlined mask="#########" inputmode="numeric" bg-color="white"'
                    )
                ).style(
                    "transition: 0.5s;transition-timing-function:"
                    "cubic-bezier(0.4, 0, 0.2, 1);"
                )

                with league_id_input.add_slot("prepend"):
                    ui.icon("leaderboard")

                manager_select = (
                    ui.select(
                        options=[],
                        label="Manager",
                        with_input=True,
                    )
                    .classes("manager_select_class")
                    .classes("h-full w-0")
                    .props('outlined bg-color="white" behavior="menu"')
                    .style(
                        "width:0;transition: 0.5s;"
                        "transition-timing-function:cubic-bezier(0.4, 0, 0.2, 1); "
                    )
                )

        with ui.element("div").classes("w-[60px] sm:w-[80px]"):
            gameweek_select = (
                ui.select([1, 2, 3], value=1, label="GW")
                .classes("gw_select_class")
                .classes("w-full h-full")
                .props('outlined bg-color="white" behavior="menu"')
            )

    return manager_id_input, league_id_input, manager_select, gameweek_select
