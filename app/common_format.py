from contextlib import contextmanager
from router import Router
from nicegui import ui


nav_bar_whole_div = "w-full h-[70px] flex flex-row justify-between items-center mb-2"
nav_bar_hover_div = "flex flex-row items-center justify-center h-full cursor-pointer"
nav_bar_link_div = "w-auto flex flex-row justify-center justify-center h-full gap-x-1"
nav_bar_icon_div = "flex flex-row items-center justify-center sm:justify-end h-full"
nav_bar_label_div = (
    "flex flex-row items-center justify-center content-end "
    "w-full flex-1 border-b-[1px] border-slate-200 hover:border-slate-500 "
)


# Create each link in nav bar
def nav_bar_link(page_link, page_name, router):
    with ui.element("div").classes(nav_bar_hover_div) as menu_link:
        with ui.element("div").classes(nav_bar_link_div):
            with ui.element("div").classes(nav_bar_label_div):
                ui.label(page_name).classes(
                    "text-slate-600 text-center text-lg font-base mb-2"
                )

    menu_link.on("click", lambda: router.open(page_link))


def nav_bar(nav_links: list, router):
    with ui.element("div").classes(
        "w-full flex flex-row h-[100px] items-center content-center"
    ):
        with ui.element("div").classes(nav_bar_whole_div):
            with ui.element("div").classes("w-[150px] flex flex-row  ml-[20px]"):
                logo = ui.image(
                    "https://i.ibb.co/Kzfxsyc/FPLCOMPARE-grey-ball-3-ver2-slate-1.png"
                ).classes("w-[175px] absolute top-8 left-6 hover:cursor-pointer")
                logo.on("click", lambda: router.open(nav_links[0][0]))

            with ui.element("div").classes(
                "h-[70px] flex flex-row justify-center items-center gap-x-4 mr-6"
            ):
                menu_state = {"state": False}

                def menu_open_func():
                    menu_state["state"] = not menu_state["state"]

                burger = ui.icon("menu", color="slate-900").classes(
                    "text-5xl absolute top-6 right-8 lg:right-12 hover:cursor-pointer"
                )
                close = ui.icon("close", color="slate-900").classes(
                    "text-5xl absolute top-6 right-8 lg:right-12 hover:cursor-pointer"
                )

                with ui.element("div").classes(
                    "w-1/5 min-w-[300px] h-screen absolute top-0 right-0 "
                ):
                    ui.element("div").classes("h-[10vh] w-full border-2 border-black ")
                    ui.element("div").classes("h-[90vh] w-full border-2 border-black ")
                close.bind_visibility_from(menu_state, "state")
                burger.bind_visibility_from(
                    menu_state, "state", backward=lambda x: not x
                )

                burger.on("click", lambda x: menu_open_func())
                close.on("click", lambda x: menu_open_func())


def new_nav_bar():
    with ui.element("div").classes("w-screen h-[100px] absolute top-0 left-0"):
        ui.image(
            "https://i.ibb.co/Kzfxsyc/FPLCOMPARE-grey-ball-3-ver2-slate-1.png"
        ).classes("w-[175px] absolute top-8 left-6 hover:cursor-pointer")
        # logo.on("click", lambda: router.open(nav_links[0][0]))

        menu_state = {"state": False}

        def menu_open_func():
            menu_state["state"] = not menu_state["state"]
            if menu_state["state"]:
                burger_1.style("transform: translate(0px, 0px) rotate(0deg)")
                burger_2.style("opacity:1;transform: translate(0px, 10px)")
                burger_3.style("transform: translate(0px, 20px) rotate(0deg)")
            else:
                burger_1.style("transform: translate(0px, 10px) rotate(45deg);")
                burger_2.style("opacity:0; transform: translate(0px, 10px)")
                burger_3.style("transform: translate(0px, 10px) rotate(-45deg);")

        with ui.element("div").classes(
            "w-[40px] h-[40px] absolute top-9 right-[5vw] hover:cursor-pointer block"
        ) as burger_menu:
            burger_1 = ui.label().classes(
                "absolute w-[40px] h-1 bg-zinc-900 block transform transition "
                "duration-500 ease-in-out"
            )
            burger_2 = ui.label().classes(
                "absolute w-[40px] h-1 bg-zinc-900 block transform transition "
                "duration-500 ease-in-out "
            )
            burger_3 = ui.label().classes(
                "absolute w-[40px] h-1 bg-zinc-900 block transform transition "
                "duration-500 ease-in-out"
            )

        menu_open_func()
        burger_menu.on("click", lambda x: menu_open_func())

        # for page in nav_links:
        #     nav_bar_link(page[0], page[1], router)


def display(nav_links: list, router):
    # with ui.element("div").classes("w-screen h-[100px] absolute top-0 left-0"):
    #     nav_bar(nav_links, router)
    new_nav_bar()
    return
