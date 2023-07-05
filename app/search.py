from nicegui import ui
import asyncio
from squad_display import show_squad

from fpl_api_getters import get_mini_league_managers, get_mini_league_managers_async


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
        "row row-flex items-center justify-center w-full h-full"
    ):
        with ui.element("div").classes(
            "row row-flex items-center justify-center w-full max-w-[500px] h-full"
        ):
            with ui.element("div").classes(
                (
                    "row row-flex items-center justify-center w-full max-w-[500px] "
                    "h-full overflow-hidden"
                )
            ):

                def stepper_navigation_foward():
                    step_1.style("translate:0px -100%")
                    step_2.style("translate:0px -100%")

                def stepper_navigation_backward():
                    step_1.style("translate:0px 0px")
                    step_2.style("translate:0px 0px")

                with ui.element("div").classes(
                    (
                        "flex flex-row w-full h-full items-center content-center "
                        "justify-center"
                    )
                ).style(
                    (
                        "transition-duration: 300ms; transition-delay: 250ms; "
                        "transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);"
                    )
                ) as step_1:
                    add_mini_league = (
                        ui.input("Mini League ID")
                        .classes("w-full")
                        .props(
                            (
                                'clearable outlined color="blue-grey" '
                                'mask="############" inputmode="numeric"'
                            )
                        )
                    )

                    next_button = (
                        ui.button(
                            icon="expand_more", on_click=stepper_navigation_foward
                        )
                        .classes("w-full animate-bounce")
                        .props("flat")
                    )
                    next_button.set_visibility(False)

                with ui.element("div").classes(
                    "w-full h-full flex flex-row items-center justify-center"
                ).style(
                    (
                        "transition-duration: 300ms; transition-delay: 250ms; "
                        "transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);"
                    )
                ) as step_2:

                    async def add_league_managers(league_id: int):
                        if not league_id:
                            with add_mini_league.add_slot("append"):
                                with ui.icon("error", color="red-500"):
                                    ui.tooltip("Please enter a League ID").classes(
                                        "bg-red-500"
                                    )
                                add_mini_league.update()
                            return

                        manager_1_input.clear()
                        manager_2_input.clear()

                        manager_1_input.set_value(value=None)
                        manager_2_input.set_value(value=None)

                        managers = await get_mini_league_managers(league_id)

                        if managers:
                            with add_mini_league.add_slot("append"):
                                ui.icon("check_circle", color="green-500")
                                add_mini_league.update()
                        else:
                            with add_mini_league.add_slot("append"):
                                with ui.icon("error", color="red-500"):
                                    ui.tooltip("Invalid League ID").classes(
                                        "bg-red-500"
                                    )
                                add_mini_league.update()
                            return
                        stepper_navigation_foward()

                        manager_1_input.options = managers
                        manager_2_input.options = managers
                        manager_1_input.update()
                        manager_2_input.update()
                        next_button.set_visibility(True)

                    def check_valid():
                        state["valid"] = manager_1_input.value and manager_2_input.value

                    state = {"valid": False}

                    ui.button(
                        icon="expand_less", on_click=stepper_navigation_backward
                    ).classes("w-full animate-bounce").props("flat")

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
                        .props(
                            'color="red-6" outlined behavior="menu" append-icon-right'
                        )
                    )

                    add_mini_league.on(
                        "keydown.enter",
                        lambda: add_league_managers(add_mini_league.value),
                        throttle=2.0,
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


async def top_50_search():
    top_50_managers = await get_mini_league_managers(314, 1)

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
                ui.button("Compare")
                .classes("w-1/4 h-[55px]")
                .props('color="blue-grey" outline')
                .bind_enabled_from(state, "valid")
            )

    return manager_1_input, manager_2_input, gameweek_select, search_button


def search(
    tab,
    manager_id_1,
    manager_id_2: int,
    gameweek: int,
    search_button,
    complete_div,
):
    search_button.on(
        "click",
        lambda: show_squad(
            tab,
            complete_div,
            manager_id_1,
            manager_id_2,
            gameweek.value,
        ),
        throttle=2.0,
    )
