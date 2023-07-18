from nicegui import ui
import asyncio

import fpl_api_getters
from player import Player
from custom_components import input_with_select, league_search
from generate_squad import generate_squad, manager_summary


def manager_chip(manager_name: str, home: bool):
    if home:
        chip_bg = " bg-sky-500 outline-sky-500"
    else:
        chip_bg = " bg-red-500 outline-red-500"

    with ui.element("div").classes(
        "w-[210px] h-[40px] rounded-lg outline outline-offset-4 relative" + chip_bg
    ) as chip:
        gw_chip_label = ui.label("21").classes(
            "w-[22px] h-[22px] rounded-full "
            "bg-slate-600 text-white absolute -top-[13px] -left-[10px] text-center "
            "font-semibold align-middle"
        )
        with ui.row().classes(
            "w-full h-full flex flex-row justify-between content-center items-center"
        ):
            manager_name = ui.label(manager_name).classes(
                "text-white pl-2 max-w-[150px] h-[20px] font-semibold text-md"
            )
            delete_chip = ui.icon("cancel", size="25px").classes(
                "cursor-pointer pr-2 text-slate-50 hover:text-slate-400"
            )

    chip.style("visibility:hidden")

    return chip, manager_name, delete_chip, gw_chip_label


async def show_page():
    with ui.element("div").classes("flex flex-row"):
        with ui.element("div").classes(
            (
                "flex flex-row justify-center items-center content-center h-screen "
                "w-screen bg-transparent"
            )
        ) as landing_div:
            with ui.element("div").classes("h-1/5 w-full flex flex-row"):
                ui.label()

            with ui.element("div").classes(
                "h-1/4 w-full flex flex-row justify-center content-end items-center "
                "pb-6 gap-x-2"
            ):
                compare_button = (
                    ui.button("Compare", color="white")
                    .classes("compare_button_class")
                    .classes("text-5xl sm:text-6xl font-sans font-bold mt-2")
                    .props('push color="white" :ripple="{ center: true }"')
                )
                ui.label("Squads.").classes(
                    "text-5xl sm:text-6xl text-zinc-900 font-sans font-bold h-auto "
                    "w-auto text-center align-middle"
                )

            search_toggle = (
                ui.switch()
                .classes("absolute top-[85vh] right-[5px]")
                .props('size="70px" checked-icon="leaderboard" unchecked-icon="person"')
            )
            with ui.element("div").classes(
                "h-1/4 w-full flex flex-row content-start justify-center relative mx-2"
            ):
                input_1, gw_select_1 = input_with_select()

                input_1.classes("flex-grow min-w-[100px]")
                gw_select_1.classes("w-[60px] sm:w-[80px]")

                (
                    league_input,
                    manager_select_input,
                    gw_select_2,
                    league_search_div,
                ) = league_search()

                gw_select_2.classes("w-[60px] sm:w-[80px]")
                manager_select_input.style(
                    "width:0;transition: 0.5s;"
                    "transition-timing-function:cubic-bezier(0.4, 0, 0.2, 1); "
                )
                league_input.classes("flex-grow shrink").style(
                    "transition: 0.5s;"
                    "transition-timing-function:cubic-bezier(0.4, 0, 0.2, 1);"
                )

                league_search_div.classes("absolute top-0 z-100")
                gw_select_2.bind_visibility_from(search_toggle, "value")
                league_input.bind_visibility_from(search_toggle, "value")
                manager_select_input.bind_visibility_from(search_toggle, "value")

                async def search_league(league_id):
                    if not league_id:
                        with league_input.add_slot("prepend"):
                            with ui.icon("error", color="red-500"):
                                ui.tooltip("Please enter a League ID").classes(
                                    "bg-red-500"
                                )
                            league_input.update()
                        return

                    manager_select_input.clear()

                    manager_select_input.set_value(value=None)

                    managers = await fpl_api_getters.get_mini_league_managers(
                        int(league_id)
                    )

                    managers = {
                        12313: "Ujedinjeni Urci",
                        2131: "Badger Oblong Quasi",
                        3763: "Bad Team On Paper",
                    }

                    if managers:
                        with league_input.add_slot("prepend"):
                            ui.icon("check_circle", color="green-500")
                            manager_select_input.style("width:50%;")
                            manager_select_input.update()
                            league_input.style("width:30%;")
                            league_input.update()
                    else:
                        with league_input.add_slot("prepend"):
                            with ui.icon("error", color="red-500"):
                                ui.tooltip("Invalid League ID").classes("bg-red-500")
                            league_input.update()
                        return

                    manager_select_input.options = managers
                    manager_select_input.update()

                league_input.on(
                    "keydown.enter", lambda: search_league(league_input.value)
                )

                gw_select_1.bind_value(gw_select_2, "value")

                chip_state = {
                    "chip_1": None,
                    "chip_2": None,
                    "chip_1_id": None,
                    "chip_2_id": None,
                    "chip_1_gw": None,
                    "chip_2_gw": None,
                }

                def add_chip(manager_id, gw_select_1):
                    if manager_id and gw_select_1:
                        if not chip_state["chip_1"]:
                            manager_name = fpl_api_getters.manager_name(manager_id)
                            if manager_name:
                                chip_state["chip_1_id"] = int(manager_id)
                                chip_state["chip_1"] = manager_name
                                chip_state["chip_1_gw"] = gw_select_1
                                chip_1.style("visibility:visible")
                                input_1.set_value("")

                            else:
                                ui.notify("Manager does not exist", closeBtn="OK")
                        elif not chip_state["chip_2"]:
                            manager_name = fpl_api_getters.manager_name(manager_id)
                            if manager_name:
                                chip_state["chip_2_id"] = int(manager_id)
                                chip_state["chip_2"] = manager_name
                                chip_state["chip_2_gw"] = gw_select_1
                                chip_2.style("visibility:visible")
                                input_1.set_value("")
                            else:
                                ui.notify("Manager does not exist", closeBtn="OK")
                    else:
                        pass

                def delete_chip(chip):
                    if chip == chip_1:
                        chip_state["chip_1"] = None
                    else:
                        chip_state["chip_2"] = None

                    chip.style("visibility:hidden")

                with ui.element("div").classes(
                    "w-full flex flex-row justify-center content-start gap-x-4 gap-y-6 "
                    "pt-6"
                ):
                    (
                        chip_1,
                        manager_name_1,
                        delete_chip_1,
                        gw_chip_label_1,
                    ) = manager_chip("WHU Tang Clan", True)
                    (
                        chip_2,
                        manager_name_2,
                        delete_chip_2,
                        gw_chip_label_2,
                    ) = manager_chip("Ruislip Rejects", False)

                    gw_chip_label_1.bind_text_from(chip_state, "chip_1_gw")
                    gw_chip_label_2.bind_text_from(chip_state, "chip_2_gw")

                    manager_name_1.bind_text_from(chip_state, "chip_1")
                    manager_name_2.bind_text_from(chip_state, "chip_2")

            async def manager_id_search():
                if chip_state["chip_1"] and chip_state["chip_2"]:
                    await generate_squad(
                        chip_state,
                        display_div,
                        landing_div,
                        summary_state,
                        squad_1_display,
                        squad_2_display,
                        bench_1_display,
                        bench_2_display,
                    )
                else:
                    ui.notify("Please enter 2 manager IDs", closeBtn="OK")

            ui.element("div").classes(
                "h-1/6 w-full flex flex-row content-start justify-center"
            )

            compare_button.on("click", manager_id_search)
            delete_chip_1.on("click", lambda x: delete_chip(chip_1))
            delete_chip_2.on("click", lambda x: delete_chip(chip_2))

            input_1.on(
                "keydown.enter", lambda x: add_chip(input_1.value, gw_select_1.value)
            )

            manager_select_input.on(
                "update:model-value",
                lambda x: add_chip(manager_select_input.value, gw_select_2.value),
            )

        with ui.element("div").classes(
            (
                "flex flex-row justify-center content-center min-h-screen "
                " w-full bg-stone-100 "
                " gap-y-0 overflow-hidden gap-x-10 relative"
            )
        ) as display_div:
            ui.label().classes("w-11/12 h-2 bg-slate-900")
            ui.label("Squads.").classes(
                "text-6xl sm:text-7xl text-slate-900 font-sans font-bold h-auto "
                "w-auto text-center align-middle mb-6 mt-1"
            )

            with ui.element("div").classes(
                "w-full h-auto flex flex-row justify-evenly content-center mx-2 "
                "lg:gap-x-0 mb-4 gap-y-2"
            ):
                manager_name_1, manager_points_1 = manager_summary(True)
                manager_name_2, manager_points_2 = manager_summary(False)

            summary_state = {
                "manager_name_1": "",
                "manager_1_points": 0,
                "manager_name_2": "",
                "manager_2_points": 0,
            }
            manager_name_1.bind_text_from(summary_state, "manager_name_1")
            manager_name_2.bind_text_from(summary_state, "manager_name_2")
            manager_points_1.bind_text_from(summary_state, "manager_1_points")
            manager_points_2.bind_text_from(summary_state, "manager_2_points")

            with ui.element("div").classes(
                "flex flex-row justify-center  gap-x-4 gap-y-2 mb-2"
            ):
                with ui.element("div").classes(
                    "flex flex-row  content-center items-center "
                ):
                    ui.icon("copyright", color="zinc-900", size="sm")
                    ui.label("Captain").classes("ml-1")
                with ui.element("div").classes(
                    "flex flex-row  content-center items-center "
                ):
                    ui.icon("local_fire_department", color="zinc-900", size="sm")
                    ui.label("Triple Captain").classes("ml-1")
                with ui.element("div").classes(
                    "flex flex-row  content-center items-center"
                ):
                    ui.icon("add_circle", color="zinc-900", size="sm")
                    ui.label("Auto sub in").classes("ml-1")
                with ui.element("div").classes(
                    "flex flex-row  content-center items-center"
                ):
                    ui.icon("do_not_disturb_on", color="zinc-900", size="sm")
                    ui.label("Auto sub out").classes("ml-1 ")

            with ui.element("div").classes(
                "mx-[4px] w-full gap-x-10 flex flex-row justify-center content-center "
                " mb-2"
            ):
                with ui.element("div").classes(
                    "px-2 pt-2 lg:pb-2 w-full max-w-[490px] "
                    "bg-gradient-to-b from-green-400 via-emerald-400 to-emerald-500"
                    " rounded-t-xl lg:rounded-b-xl"
                ):
                    with ui.image(
                        "https://i.ibb.co/xS9j0v0/half-pitch-complete-final-4.png"
                    ).classes("max-w-[482px] w-full"):
                        squad_1_display = ui.element("div").classes(
                            "w-full h-full gap-y-0 bg-transparent flex flex-row "
                            "content-start "
                        )
                with ui.element("div").classes(
                    "px-2 lg:pt-2 pb-2 w-full max-w-[490px]  "
                    "lg:bg-gradient-to-b lg:from-green-400 lg:via-emerald-400 "
                    "lg:to-emerald-500 rounded-b-xl lg:rounded-t-xl "
                    "bg-gradient-to-b from-emerald-500 via-emerald-400 to-green-400"
                ):
                    with ui.image(
                        "https://i.ibb.co/xS9j0v0/half-pitch-complete-final-4.png"
                    ).classes("max-w-[482px] w-full rotate-180 lg:rotate-0"):
                        squad_2_display = ui.element("div").classes(
                            "w-full h-full gap-y-1 flex flex-row bg-transparent"
                        )
            with ui.element("div").classes(
                "w-full  flex flex-row justify-center content-center gap-x-10 mb-4 "
                "mx-2 gap-y-2"
            ):
                with ui.element("div").classes(
                    "w-full max-w-[490px] p-1 bg-gradient-to-r rounded-2xl "
                    "from-sky-500 via-sky-300 to-cyan-400 drop-shadow-xl "
                ):
                    bench_1_display = ui.element("div").classes(
                        "w-full max-w-[490px] h-[100px] flex flex-row justify-evenly "
                        "bg-slate-50/50 content-center rounded-xl"
                    )

                with ui.element("div").classes(
                    "w-full max-w-[490px] p-1 bg-gradient-to-r rounded-2xl "
                    "from-red-500 via-red-400 to-rose-400 drop-shadow-xl"
                ):
                    bench_2_display = ui.element("div").classes(
                        "w-full  max-w-[490px] h-[100px] flex flex-row justify-evenly "
                        "bg-slate-50/50 content-center rounded-xl opac"
                    )

            with ui.element("div").classes(
                "w-full h-screen bg-stone-100 flex row-flex justify-center "
                "content-start"
            ):
                ui.label().classes("w-11/12 h-2 bg-slate-900")
                ui.label("Transfers.").classes(
                    "text-5xl sm:text-7xl text-slate-900 font-sans font-bold "
                    "w-auto text-center align-middle mb-10 "
                )

        display_div.set_visibility(False)
