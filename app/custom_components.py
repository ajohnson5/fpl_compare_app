from nicegui import ui


def input_with_select():
    with ui.element("div").classes(
        "flex flex-row gap-x-0 w-full content-center justify-center mx-2"
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
            ui.select([0, 1, 2, 3], label="GW")
            .classes("gw_select_class")
            .props('outlined bg-color="white"')
        )

    return input, select
