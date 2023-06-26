from contextlib import contextmanager
import page_creation

from nicegui import ui


nav_bar_whole_div = (
    "w-full h-[70px] flex flex-row justify-center items-center"
    " sm:justify-start mb-2 divide-slate-100 divide-x-2"
)
nav_bar_hover_div = (
    "flex flex-row items-center justify-center w-1/4"
    " h-full bg-slate-500 cursor-pointer hover:bg-slate-400"
)
nav_bar_link_div = (
    "flex flex-row grid grid-cols-1 grid-rows-3 sm:grid-cols-2"
    " sm:grid-rows-1 justify-center w-[200px] h-full gap-x-1"
)
nav_bar_icon_div = (
    "flex flex-row col-span-1 row-span-2 sm:row-span-1"
    " items-center justify-center sm:justify-end h-full"
)
nav_bar_label_div = (
    "flex flex-row col-span-1 row-span-1 items-center justify-center"
    " sm:justify-start h-full"
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
            with ui.element("div").classes(nav_bar_icon_div):
                ui.icon(icon).classes("text-5xl absolute text-slate-100")
            with ui.element("div").classes(nav_bar_label_div):
                ui.label(page_name).classes("text-slate-100")
    menu_link.on("click", lambda: ui.open(link))


def nav_bar():
    with ui.element("div").classes(nav_bar_whole_div):
        for page in nav_bar_pages:
            nav_bar_link(page[0], page[1], page[2])


@contextmanager
def display():
    with ui.element("div").classes("w-full h-full left-0 top-0 absolute"):
        nav_bar()

        yield
