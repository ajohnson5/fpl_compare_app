from nicegui import ui, app
import asyncio

from layout_components import home_logo

nav_bar_hover_div = (
    "flex flex-row items-center justify-center cursor-pointer w-full "
    "h-1/6 min-h-[70px] sm:px-4 hover:bg-stone-200"
)
nav_bar_link_div = "w-full flex flex-row justify-center justify-center"
nav_bar_icon_div = "flex flex-row items-center justify-center sm:justify-end h-full"
nav_bar_label_div = (
    "flex flex-row items-center justify-center content-end "
    "w-full flex-1 border-b-[1px] border-slate-200 hover:border-slate-500 "
)


def nav_bar():
    with ui.element("div").classes("w-screen h-[100px] absolute top-0 left-0 z-30"):
        # Add FPL logo to use as a home button
        with ui.link(target="/").classes("z-30"):
            (
                ui.html(home_logo)
                .classes("w-[110px] absolute top-8 left-6 hover:cursor-pointer z-30")
                .props("no-spinner")
            )

        # Dict to track if menu is open or not
        menu_state = {"state": True}

        # Javascript to set burger menu to fixed when side bar is open
        async def overflow_off():
            await ui.run_javascript(
                f"getElement({burger_menu.id}).style.position = 'fixed'"
            )
            await ui.run_javascript(f'getElement({side_bar.id}).className ="side_bar"')

        # Javascript to set burger menu to absolute when side bar is closed
        async def overflow_on():
            await ui.run_javascript(
                f"getElement({burger_menu.id}).style.position = 'absolute'"
            )
            await ui.run_javascript(f'getElement({side_bar.id}).className =""')

        # Transform burger to cross when menu is open and vice versa when closed
        async def menu_open_func():
            menu_state["state"] = not menu_state["state"]
            if menu_state["state"]:
                burger_1.style("transform: translate(0px, 0px) rotate(0deg);")
                burger_2.style("opacity:1;transform: translate(0px, 10px)")
                burger_3.style("transform: translate(0px, 20px) rotate(0deg);")
                await overflow_on()
            else:
                burger_1.style("transform: translate(0px, 10px) rotate(45deg);")
                burger_2.style("opacity:0; transform: translate(0px, 10px)")
                burger_3.style("transform: translate(0px, 10px) rotate(-45deg);")
                await overflow_off()

        # Create burger for side bar
        with ui.element("div").classes(
            "w-[40px] h-[40px] absolute top-9 left-[85vw] md:left-[95vw] z-30 "
            "hover:cursor-pointer block"
        ) as burger_menu:
            burger_1 = ui.label().classes(
                "absolute w-[40px] h-1 bg-stone-700 block transform transition "
                "duration-500 ease-in-out"
            )
            burger_2 = (
                ui.label()
                .classes(
                    "absolute w-[40px] h-1 bg-stone-700 block transform transition "
                    "duration-500 ease-in-out "
                )
                .style("transform: translate(0px, 10px)")
            )
            burger_3 = (
                ui.label()
                .classes(
                    "absolute w-[40px] h-1 bg-stone-700 block transform transition "
                    "duration-500 ease-in-out"
                )
                .style("transform: translate(0px, 20px)")
            )

        # Create side bar which slides in from right
        with ui.element("div").style(
            "height: 100vh;width: 0;position: fixed; "
            "z-index: 20;top: 0;right: 0;background-color:white; overflow: hidden; "
            "transition: 0.5s;transition-timing-function:cubic-bezier(0.4, 0, 0.2, 1); "
            "padding-top: 110px;text-align:center;filter: "
            "drop-shadow(0 20px 13px rgb(0 0 0 / 0.03)) "
            "drop-shadow(0 8px 5px rgb(0 0 0 / 0.08));"
        ).classes("drop-shadow-xl ") as side_bar:
            # Add manager and league id store where previously entered IDs to be reused
            with ui.element("div").classes(
                "w-full h-full flex flex-col content-around justify-around"
            ):
                with ui.element("div").classes("w-full flex flex-row "):
                    ui.label("Past Managers").classes(
                        "w-full text-center text-2xl font-bold"
                    )
                    manager_id_store = ui.scroll_area().classes(
                        "w-full grid grid-cols-1 gap-y-2 p-4 h-1/3 min-h-[200px] "
                        "sm:min-h-[250px] border-2 border-double border-stone-300 "
                        "rounded-xl p-2 mx-2"
                    )

                with ui.element("div").classes("w-full flex flex-row"):
                    ui.label("Past Leagues").classes(
                        "w-full text-center text-2xl font-bold"
                    )
                    league_id_store = ui.scroll_area().classes(
                        "w-full grid grid-cols-1 gap-y-2 p-4 h-1/3 min-h-[200px] "
                        "sm:min-h-[250px] border-2 border-double border-stone-300 "
                        "rounded-xl p-2 mx-2"
                    )

                # GitHub link to my repo
                with ui.element("div").classes(
                    "w-full flex flex-row content-center justify-center"
                ):
                    with ui.link(target="https://github.com/ajohnson5"):
                        ui.element("i").classes("eva eva-github").classes(
                            "text-5xl hover:scale-105 hover:cursor-pointer "
                            "text-stone-900"
                        )

    burger_menu.on("click", lambda x: menu_open_func())

    return side_bar, manager_id_store, league_id_store


def display():
    ui.element("div").classes(
        ("h-screen w-screen bg-stone-100 " "absolute top-0 left-0 -z-10")
    )
    return nav_bar()
