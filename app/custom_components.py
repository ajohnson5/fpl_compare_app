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
                ('outlined mask="############" inputmode="numeric" ' 'bg-color="white"')
            )
        )

        with input.add_slot("prepend"):
            ui.icon("leaderboard")

        # with input.add_slot("append"):
        #     ui.icon("check_circle",color="green-5")

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
