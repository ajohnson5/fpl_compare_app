from contextlib import contextmanager
import page_creation

from nicegui import ui


nav_bar_whole_div = "w-full h-[70px] flex flex-row justify-between items-center mb-2"
nav_bar_hover_div = (
    "flex flex-row items-center justify-center w-1/5 h-full cursor-pointer"
)
nav_bar_link_div = (
    "flex flex-row justify-center justify-center w-[200px] h-full gap-x-1"
)
nav_bar_icon_div = "flex flex-row" " items-center justify-center sm:justify-end h-full"
nav_bar_label_div = (
    "flex flex-row items-center justify-center content-end "
    "w-full flex-1 border-b-[1px] border-slate-200 hover:border-slate-500 "
)


# List of all nav bar links with icon, page_name and link
nav_bar_pages = [
    ("home", "Home", page_creation.home_page),
    ("group", "Manager ID", page_creation.by_manager_id_page),
    ("leaderboard", "Mini-league", page_creation.by_mini_league_page),
    ("looks_5", "Top 5", page_creation.by_top_5_page),
]


# Create each link in nav bar
def nav_bar_link(icon: str, page_name: str, link):
    with ui.element("div").classes(nav_bar_hover_div) as menu_link:
        with ui.element("div").classes(nav_bar_link_div):
            with ui.element("div").classes(nav_bar_label_div):
                ui.label(page_name).classes(
                    "text-slate-600 text-center text-lg font-base mb-2"
                )
    menu_link.on("click", lambda: ui.open(link))


def nav_bar():
    with ui.element("div").classes(
        "w-full flex flex-row h-[110px] items-center content-center"
    ):
        with ui.element("div").classes(nav_bar_whole_div):
            with ui.element("div").classes("w-[150px] flex flex-row  ml-[20px]"):
                ui.image("https://i.ibb.co/DgpgtXN/FPLCOMPARE.png").classes("w-[150px]")
            with ui.element("div").classes(
                "w-1/2 h-[70px] flex flex-row justify-center items-center  mr-6 gap-x-4"
            ):
                for page in nav_bar_pages:
                    nav_bar_link(page[0], page[1], page[2])


@contextmanager
def display():
    with ui.element("div").classes("w-full h-full left-0 top-0 absolute"):
        nav_bar()

        yield
