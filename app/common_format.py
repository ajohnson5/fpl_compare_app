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
        "w-full flex flex-row h-[110px] items-center content-center"
    ):
        with ui.element("div").classes(nav_bar_whole_div):
            with ui.element("div").classes("w-[150px] flex flex-row  ml-[20px]"):
                logo = ui.image("https://i.ibb.co/DgpgtXN/FPLCOMPARE.png").classes(
                    "w-[150px] hover:cursor-pointer"
                )
                logo.on("click", lambda: router.open(nav_links[0][0]))

            with ui.element("div").classes(
                "h-[70px] flex flex-row justify-center items-center gap-x-4 mr-6"
            ):
                for page in nav_links:
                    nav_bar_link(page[0], page[1], router)


def display(nav_links: list, router):
    with ui.element("div").classes("w-full h-full"):
        nav_bar(nav_links, router)
    return
