from nicegui import ui


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


def manager_chip(home: bool):
    if home:
        chip_bg = " bg-sky-500 outline-sky-500"
    else:
        chip_bg = " bg-red-500 outline-red-500"

    with ui.element("div").classes(
        "w-[210px] h-[40px] rounded-lg outline outline-offset-4 relative" + chip_bg
    ) as chip:
        gw_chip_label = ui.label().classes(
            "w-[22px] h-[22px] rounded-full bg-slate-600 text-white absolute "
            "-top-[13px] -left-[10px] text-center font-semibold align-middle"
        )
        with ui.row().classes(
            "w-full h-full flex flex-row justify-between content-center items-center"
        ):
            manager_name = ui.label().classes(
                "text-white pl-2 max-w-[150px] h-[20px] font-semibold text-md"
            )
            delete_chip = ui.icon("cancel", size="25px").classes(
                "cursor-pointer pr-2 text-slate-50 hover:text-slate-400"
            )

    chip.style("visibility:hidden")

    return chip, manager_name, delete_chip, gw_chip_label
