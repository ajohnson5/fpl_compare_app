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
                        'clearable outlined inputmode="search" mask="##########" '
                        'bg-color="white"'
                    )
                )
            )

            with manager_id_input.add_slot("prepend"):
                ui.icon("search")

            with ui.element("div").classes(
                "absolute top-0 left-0 w-full z-10 overflow-hidden flex flex-row"
            ):
                league_id_input = (
                    ui.input("League ID")
                    .classes("input_class")
                    .classes("h-full")
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

                manager_select = (
                    ui.select(
                        options=[],
                        label="Manager",
                        with_input=False,
                    )
                    .classes("manager_select_class")
                    .classes("h-full")
                    .props('outlined bg-color="white" behavior="menu"')
                    .style(
                        "width:0;transition:width 0.5s cubic-bezier(0.4, 0, 0.2, 1);"
                        "-webkit-transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1); "
                        "-moz-transition:width 0.5s cubic-bezier(0.4, 0, 0.2, 1); "
                        "-o-transition:width 0.5s cubic-bezier(0.4, 0, 0.2, 1); "
                    )
                )

        with ui.element("div").classes("w-[60px] sm:w-[80px]"):
            gameweek_select = (
                ui.select([x for x in range(1, 6)], value=5, label="GW")
                .classes("gw_select_class")
                .classes("w-full h-full")
                .props('outlined bg-color="white" behavior="menu"')
            )

    return manager_id_input, league_id_input, manager_select, gameweek_select


def manager_chip(home: bool):
    if home:
        chip_bg = " from-sky-500 via-sky-300 to-cyan-400"
    else:
        chip_bg = " from-red-500 via-red-400 to-rose-400"

    with ui.element("div").classes(
        "p-1 bg-white  rounded-xl drop-shadow-xl hover:cursor-pointer"
    ) as chip:
        with ui.element("div").classes(
            "w-[190px] h-[40px] rounded-lg relative bg-gradient-to-r " + chip_bg
        ):
            with ui.row().classes(
                "w-full h-full flex flex-row justify-start content-center "
                "items-center divide-x-4 divide-white gap-x-0"
            ):
                gw_chip_label = ui.label().classes(
                    "text-stone-100 w-1/5 min-w-[35px] font-semibold text-lg "
                    "text-center "
                )
                with ui.element("div").classes(
                    "h-full flex flex-row justify-start content-center grow"
                ):
                    manager_name = (
                        ui.label()
                        .classes(
                            "text-stone-100 w-[140px] font-semibold text-md "
                            "text-center pl-1"
                        )
                        .style(
                            "overflow:hidden;white-space: nowrap;text-overflow: "
                            "ellipsis;display: block; "
                        )
                    )

    chip.style("visibility:hidden")

    return chip, manager_name, gw_chip_label


def create_button(button_label: str):
    button = ui.html(
        f"""
    <button class="pushable">
        <span class="shadow"></span>
        <span class="edge"></span>
        <span class="front">
            {button_label}
        </span>
    </button>
    """
    )

    return button


formations = {
    "352": [1, 3, 5, 2],
    "343": [1, 3, 4, 3],
    "451": [1, 4, 5, 1],
    "442": [1, 4, 4, 2],
    "433": [1, 4, 3, 3],
    "541": [1, 5, 4, 1],
    "532": [1, 5, 3, 2],
    "523": [1, 5, 2, 3],
}

formation_index = {
    1: "Squad",
    2: "352",
    3: "343",
    4: "451",
    5: "442",
    6: "433",
    7: "541",
    8: "532",
    9: "523",
}


def formation_select():
    ui.select(
        options=formation_index,
        value=formation_index[1],
    ).props("rounded outlined")
