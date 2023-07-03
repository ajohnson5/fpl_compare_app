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

            def check_valid():
                state["valid"] = manager_1_input.value and manager_2_input.value

            state = {"valid": False}

            manager_1_input = (
                ui.input("Manager ID 1", on_change=check_valid)
                .classes("w-3/4 pr-2 pb-2")
                .props(
                    (
                        'clearable outlined color="blue-6" mask="############"'
                        ' inputmode="numeric"'
                    )
                )
            )

            gameweek_select = (
                ui.select([x for x in range(1, 39)], value=38, label="GW")
                .classes("w-1/4 pb-2")
                .props('outlined behavior="menu" color="blue-grey"')
            )

            manager_2_input = (
                ui.input("Manager ID 2", on_change=check_valid)
                .classes("w-3/4 pr-2")
                .props(
                    (
                        'clearable outlined color="red-6" mask="############" '
                        'inputmode="numeric"'
                    )
                )
            )

            search_button = (
                ui.button(
                    "Compare",
                )
                .classes("w-1/4 h-[55px]")
                .props('color="blue-grey" outline')
                .bind_enabled_from(state, "valid")
            )

    return manager_1_input, manager_2_input, gameweek_select, search_button


def mini_league_search_bar():
    with ui.element("div").classes(
        "row row-flex items-center justify-center w-full p-2"
    ):
        with ui.element("div").classes(
            "row row-flex items-center justify-center w-full max-w-[500px]"
        ):
            add_mini_league = (
                ui.input("Mini League ID")
                .classes("w-full pb-2")
                .props(
                    (
                        'clearable outlined color="blue-grey" mask="############" '
                        'inputmode="numeric"'
                    )
                )
            )

            def add_league_managers(league_id: int):
                manager_1_input.clear()
                manager_2_input.clear()

                manager_1_input.set_value(value=None)
                manager_2_input.set_value(value=None)

                managers = get_mini_league_managers(league_id)
                manager_1_input.options = managers
                manager_2_input.options = managers
                manager_1_input.update()
                manager_2_input.update()

            def check_valid():
                state["valid"] = manager_1_input.value and manager_2_input.value

            state = {"valid": False}

            manager_1_input = (
                ui.select(
                    value=None,
                    options={},
                    with_input=True,
                    label="Manager 1 Name",
                    on_change=check_valid,
                )
                .classes("w-3/4 pr-2 pb-2")
                .props('color="blue-6" outlined behavior="menu"')
            )

            gameweek_select = (
                ui.select([x for x in range(1, 39)], value=38, label="GW")
                .classes("w-1/4 pb-2")
                .props('outlined behavior="menu" color="blue-grey"')
            )

            manager_2_input = (
                ui.select(
                    value=None,
                    options={},
                    with_input=True,
                    label="Manager 2 Name",
                    on_change=check_valid,
                )
                .classes("w-3/4 pr-2")
                .props('color="red-6" outlined behavior="menu"')
            )

            add_mini_league.on(
                "keydown.enter",
                lambda: add_league_managers(int(add_mini_league.value)),
            )

            search_button = (
                ui.button(
                    "Compare",
                )
                .classes("w-1/4 h-[55px]")
                .props('color="blue-grey" outline')
                .bind_enabled_from(state, "valid")
            )

    return manager_1_input, manager_2_input, gameweek_select, search_button


def top_50_search():
    top_50_managers = get_mini_league_managers(314, 1)

    with ui.element("div").classes(
        "row row-flex items-center justify-center w-full p-2"
    ):
        with ui.element("div").classes(
            "row row-flex items-center justify-center w-full max-w-[500px]"
        ):

            def check_valid():
                state["valid"] = manager_1_input.value and manager_2_input.value

            state = {"valid": False}

            manager_1_input = (
                ui.input("Manager ID", on_change=check_valid)
                .classes("w-3/4 pr-2 pb-2")
                .props(
                    (
                        'clearable outlined color="blue-6" mask="############" '
                        'inputmode="numeric"'
                    )
                )
            )

            gameweek_select = (
                ui.select([x for x in range(1, 39)], value=38, label="GW")
                .classes("w-1/4 pb-2")
                .props('outlined behavior="menu" color="blue-grey"')
            )

            manager_2_input = (
                ui.select(
                    top_50_managers,
                    with_input=True,
                    label="Top Manager",
                    on_change=check_valid,
                )
                .classes("w-3/4 pr-2")
                .props('color="red-6" outlined behavior="menu"')
            )

            search_button = (
                ui.button(
                    "Compare",
                )
                .classes("w-1/4 h-[55px]")
                .props('color="blue-grey" outline')
                .bind_enabled_from(state, "valid")
            )

    return manager_1_input, manager_2_input, gameweek_select, search_button


def manager_id_search():
    manager_id_1, manager_id_2, gameweek, search_button = manager_id_search_bar()

    search(manager_id_1, manager_id_2, gameweek, search_button)


def mini_league_search():
    manager_id_1, manager_id_2, gameweek, search_button = manager_id_search_bar()

    search(manager_id_1, manager_id_2, gameweek, search_button)


def top_search():
    manager_id_1, manager_id_2, gameweek, search_button = top_50_search()

    search(manager_id_1, manager_id_2, gameweek, search_button)


def search(
    manager_id_1: int,
    manager_id_2: int,
    gameweek: int,
    search_button,
    error_message,
    complete_div,
):
    search_button.on(
        "click",
        lambda: show_squad(
            complete_div,
            error_message,
            manager_id_1.value,
            manager_id_2.value,
            gameweek.value,
        ),
    )
