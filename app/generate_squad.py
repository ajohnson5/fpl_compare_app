from nicegui import ui
import asyncio
from typing import List

import fpl_api_getters
from player import Player
from squad import Squad


async def generate_squad(
    manager_dict,
    display_div,
    loading_div,
    manager_1_display,
    manager_2_display,
    squad_1_display,
    squad_2_display,
    bench_1_display,
    bench_2_display,
    transfer_div_1,
    transfer_div_2,
):
    # Use fpl api to create squad objects for both managers
    squad_1 = fpl_api_getters.manager_gw_picks_api_temp(
        38,
        manager_dict["chip_1_id"],
        manager_dict["chip_1"],
        fpl_api_getters.squad_dict,
        fpl_api_getters.transfers,
    )
    squad_2 = fpl_api_getters.manager_gw_picks_api_temp(
        38,
        manager_dict["chip_2_id"],
        manager_dict["chip_2"],
        fpl_api_getters.squad_dict_2,
        fpl_api_getters.transfers,
    )

    # Compare squads - creates the layout instance variable
    squad_1.compare_squad(squad_2)

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

    # Create manager summary cards
    with manager_1_display:
        manager_1_display.clear()
        squad_1.create_manager_display()
    with manager_2_display:
        manager_2_display.clear()
        squad_2.create_manager_display()

    # Create player cards for on-pitch players
    with squad_1_display:
        squad_1_display.clear()
        squad_1.create_team_display("home")

    with squad_2_display:
        squad_2_display.clear()
        squad_2.create_team_display("away")

    # Create bench player cards
    with bench_1_display:
        bench_1_display.clear()
        squad_1.create_bench_display("home")

    with bench_2_display:
        bench_2_display.clear()
        squad_2.create_bench_display("away")

    # Create transfer cards
    with transfer_div_1:
        transfer_div_1.clear()
        squad_1.create_transfer_display("home")

    with transfer_div_2:
        transfer_div_2.clear()
        squad_2.create_transfer_display("away")

    display_div.set_visibility(True)
