from nicegui import ui
import asyncio

from fpl_api import (
    get_manager_gw_picks,
    squad_dict,
    squad_dict_2,
    transfers_1,
    transfers_2,
)


async def compare_squads(
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
    await asyncio.sleep(1)

    # Use fpl api to create squad objects for both managers
    squad_1 = await get_manager_gw_picks(
        manager_dict["chip_1_gw"],
        manager_dict["chip_1_id"],
        manager_dict["chip_1"],
        squad_dict,
        transfers_1,
    )

    if not squad_1:
        ui.notify(
            f'{manager_dict["chip_1"]} has no squad on Gameweek '
            f'{manager_dict["chip_1_gw"]}'
        )
        loading_clearable_div.clear()

        return

    squad_2 = await get_manager_gw_picks(
        manager_dict["chip_2_gw"],
        manager_dict["chip_2_id"],
        manager_dict["chip_2"],
        squad_dict_2,
        transfers_2,
    )
    squad_2 = None
    if not squad_2:
        ui.notify(
            f'{manager_dict["chip_2"]} has no squad on Gameweek '
            f'{manager_dict["chip_2_gw"]}'
        )
        loading_clearable_div.clear()

        return

    # Compare squads - creates the layout instance variable
    squad_1.compare_squad(squad_2)

    # Create manager summary cards
    with manager_1_display:
        manager_1_display.clear()
        squad_1.create_manager_display(manager_dict["chip_1_gw"])
    with manager_2_display:
        manager_2_display.clear()
        squad_2.create_manager_display(manager_dict["chip_2_gw"])

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

    # Clear spinner indicating the comparison is complete
    loading_clearable_div.clear()

    display_div.set_visibility(True)
