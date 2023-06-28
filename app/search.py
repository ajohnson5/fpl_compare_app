from nicegui import ui
import asyncio

from squad_display import show_squad

from fpl_api_getters import get_mini_league_managers


def manager_id_search_bar():
    with ui.element("div").classes(
        "row row-flex items-center justify-center w-full p-2"
    ):
        with ui.element("div").classes(
            "row row-flex items-center justify-center w-full max-w-[500px]"
        ):

            def check_length():
                state["enough"] = (
                    add_input.value.isdigit() and add_input_2.value.isdigit()
                )

            state = {"enough": False}

            add_input = (
                ui.input("Manager ID 1", on_change=check_length)
                .classes("w-3/4 pr-2 pb-2")
                .props('clearable outlined color="blue-6"')
            )

            gameweek_select = (
                ui.select([x for x in range(1, 39)], value=38, label="GW")
                .classes("w-1/4 pb-2")
                .props('outlined behavior="menu" color="blue-grey"')
            )

            add_input_2 = (
                ui.input("Manager ID 2", on_change=check_length)
                .classes("w-3/4 pr-2")
                .props('clearable outlined color="red-6"')
            )

            search_button = (
                ui.button(
                    "Compare",
                )
                .classes("w-1/4 h-[55px]")
                .props('color="blue-grey" outline')
                .bind_enabled_from(state, "enough")
            )

    return add_input, add_input_2, gameweek_select, search_button


def manager_id_search_bar_execute():
    add_input, add_input_2, gameweek_select, search_button = manager_id_search_bar()

    error_message = ui.element("div")

    complete_div = ui.element("div").classes("w-full h-auto")

    search_button.on(
        "click",
        lambda: show_squad(
            complete_div,
            error_message,
            add_input.value,
            add_input_2.value,
            gameweek_select.value,
        ),
    )


def create_mini_league(league_id, manager_search_div, complete_div, error_message):
    managers = get_mini_league_managers(league_id)

    if not managers:
        return ui.notify("League does not exist", type="negative", position="center")

    manager_search_div.clear()

    with manager_search_div:

        def check_manager_select():
            mini_league_select["selected"] = (
                manager_1_select.value is not None
                and manager_2_select.value is not None
            )

        mini_league_select = {"selected": False}

        manager_1_select = (
            ui.select(
                managers,
                with_input=True,
                label="Manager 1 Name",
                on_change=check_manager_select,
            )
            .classes("w-3/4 pr-2 pb-2")
            .props('color="blue-6" outlined behavior="menu"')
        )

        gameweek_select = (
            ui.select([x for x in range(1, 39)], value=38, label="GW")
            .classes("w-1/4 pb-2")
            .props('outlined behavior="menu" color="blue-grey"')
        )

        manager_2_select = (
            ui.select(
                managers,
                with_input=True,
                label="Manager 2 Name",
                on_change=check_manager_select,
            )
            .classes("w-3/4 pr-2")
            .props('color="red-6" outlined behavior="menu"')
        )

        squad_search_button = (
            ui.button(
                "Compare",
            )
            .classes("w-1/4 h-[55px]")
            .props('color="blue-grey" outline')
            .bind_enabled_from(mini_league_select, "selected")
        )

    squad_search_button.on(
        "click",
        lambda: show_squad(
            complete_div,
            error_message,
            str(manager_1_select.value),
            str(manager_2_select.value),
            gameweek_select.value,
        ),
    )


def mini_league_search_bar():
    with ui.element("div").classes("row row-flex items-center justify-center w-full"):
        with ui.element("div").classes(
            "row row-flex items-center justify-center w-full max-w-[500px]"
        ):
            with ui.element("div").classes(
                "row row-flex items-center justify-evenly w-full max-w-[500px] "
            ):
                valid = {"digits": ""}

                def valid_mini_league():
                    if not add_mini_league.value.isdigit():
                        valid["digits"] = add_mini_league.value[:-1]
                    else:
                        valid["digits"] = add_mini_league.value

                add_mini_league = (
                    ui.input("Mini League ID", on_change=valid_mini_league)
                    .classes("w-full px-2")
                    .props('clearable outlined color="blue-grey"')
                    .bind_value(valid, "digits")
                )

            manager_search_div = ui.element("div").classes(
                "row row-flex items-center justify-center w-full max-w-[500px] p-2"
            )

    error_message = ui.element("div")

    complete_div = ui.element("div").classes("w-full h-full")

    add_mini_league.on(
        "keydown.enter",
        lambda: create_mini_league(
            add_mini_league.value, manager_search_div, complete_div, error_message
        ),
    )
