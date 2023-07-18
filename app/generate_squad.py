from nicegui import ui
import asyncio
from typing import List

import fpl_api_getters
from player import Player
from squad import Squad


def row_generator_bench(player_list: List[Player], home: str):
    with ui.row().classes(
        "flex flex-row  w-full h-full justify-around content-center gap-x-0 pb-1"
    ):
        for player in player_list:
            player.create_card(home)


def row_generator(player_list: List[Player], home: str, i):
    if i == 0:
        x = "top-0"
    else:
        x = f"top-{i}/4"
    if home:
        rotate = "left-0 " + x
    else:
        rotate = " rotate-180 lg:rotate-0 left-0 " + x

    with ui.element("div").classes(
        "flex flex-row absolute w-full h-1/4 justify-around content-start gap-x-0 "
        + rotate
    ):
        for player in player_list:
            player.create_card(home)


def manager_summary(home: bool):
    if home:
        bg_color = " from-sky-500 via-sky-300 to-cyan-400 lg:mr-6"
    else:
        bg_color = " from-red-500 via-red-400 to-rose-400 lg:ml-6"
    with ui.element("div").classes(
        " p-1 bg-gradient-to-r rounded-2xl drop-shadow-xl" + bg_color
    ):
        with ui.element("div").classes(
            " w-[150px] md:w-[250px] flex flex-row justify-center "
            "content-start gap-y-1"
        ):
            with ui.element("div").classes(
                "w-full h-[50px] flex flex-row content-center rounded-t-xl "
                "bg-slate-50/30"
            ):
                manager_name = ui.label().classes(
                    "text-center w-full text-lg lg:text-2xl text-stone-100 font-medium"
                )

            with ui.element("div").classes(
                "w-full h-[100px]  flex flex-row content-center bg-slate-50/30 "
                "rounded-b-xl"
            ):
                total_points = ui.label().classes(
                    "text-center w-full text-stone-100 text-5xl md:text-7xl font-medium"
                )
                ui.label("Points").classes("text-center w-full text-stone-100")

    return manager_name, total_points


async def generate_squad(
    manager_dict,
    display_div,
    loading_div,
    summary_state,
    squad_1_display,
    squad_2_display,
    bench_1_display,
    bench_2_display,
):
    squad_1 = fpl_api_getters.manager_gw_picks_api_temp(
        38, manager_dict["chip_1_id"], fpl_api_getters.squad_dict
    )
    squad_2 = fpl_api_getters.manager_gw_picks_api_temp(
        38, manager_dict["chip_2_id"], fpl_api_getters.squad_dict_2
    )

    team_1, team_2 = squad_1.compare_squad(squad_2)

    # Create loading spinner
    with loading_div:
        with ui.element("div") as loading_clearable_div:
            with ui.element("div").classes(
                (
                    "flex flex-row w-full h-full fixed top-0 left-0 bg-stone-200/50 "
                    "items-center justify-center content-center backdrop-blur-sm z-50"
                )
            ):
                ui.spinner(size="xl", thickness=10.0)
    await asyncio.sleep(2)
    loading_clearable_div.clear()

    # Update dictionary with manager names and points
    summary_state["manager_name_1"] = manager_dict["chip_1"]
    summary_state["manager_name_2"] = manager_dict["chip_2"]
    summary_state["manager_1_points"] = squad_1.stats["points"]
    summary_state["manager_2_points"] = squad_2.stats["points"]

    # Create player cards for on-pitch players
    with squad_1_display:
        squad_1_display.clear()
        row_generator(team_1[1], "home", 0)
        row_generator(team_1[2], "home", 1)
        row_generator(team_1[3], "home", 2)
        row_generator(team_1[4], "home", 3)

    with squad_2_display:
        squad_2_display.clear()
        row_generator(team_2[1], "away", 0)
        row_generator(team_2[2], "away", 1)
        row_generator(team_2[3], "away", 2)
        row_generator(team_2[4], "away", 3)

    # Create bench player cards
    with bench_1_display:
        bench_1_display.clear()
        row_generator_bench(team_1[0], "home")

    with bench_2_display:
        bench_2_display.clear()
        row_generator_bench(team_2[0], "away")

    display_div.set_visibility(True)
