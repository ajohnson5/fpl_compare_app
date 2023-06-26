from contextlib import contextmanager
import page_creation

from nicegui import ui


nav_bar_whole_div = (
    "w-full h-[70px] flex flex-row justify-center items-center",
    " sm:justify-start mb-2 divide-slate-100 divide-x-2",
)
nav_bar_hover_div = (
    "flex flex-row items-center justify-center w-1/4",
    " h-full bg-slate-500 cursor-pointer hover:bg-slate-400",
)
nav_bar_link_div = (
    "flex flex-row grid grid-cols-1 grid-rows-3 sm:grid-cols-2",
    " sm:grid-rows-1 justify-center w-[200px] h-full gap-x-1",
)
nav_bar_icon_div = (
    "flex flex-row col-span-1 row-span-2 sm:row-span-1",
    " items-center justify-center sm:justify-end h-full",
)
nav_bar_label_div = (
    "flex flex-row col-span-1 row-span-1 items-center justify-center",
    " sm:justify-start h-full",
)


def nav_bar():
    with ui.element("div").classes(nav_bar_whole_div):
        with ui.element("div").classes(nav_bar_hover_div) as nav_0:
            with ui.element("div").classes(nav_bar_link_div):
                with ui.element("div").classes(nav_bar_icon_div):
                    ui.icon("home").classes("text-5xl absolute text-slate-100")
                with ui.element("div").classes(nav_bar_label_div):
                    ui.label("Home").classes("text-slate-100")
        nav_0.on("click", lambda: ui.open(page_creation.home_page))

        with ui.element("div").classes(nav_bar_hover_div) as nav_1:
            with ui.element("div").classes(nav_bar_link_div):
                with ui.element("div").classes(nav_bar_icon_div):
                    ui.icon("group").classes("text-5xl absolute text-slate-100")
                with ui.element("div").classes(nav_bar_label_div):
                    ui.label("Manager ID").classes("text-slate-100")
        nav_1.on("click", lambda: ui.open(page_creation.by_manager_id_page))

        with ui.element("div").classes(nav_bar_hover_div) as nav_2:
            with ui.element("div").classes(nav_bar_link_div):
                with ui.element("div").classes(nav_bar_icon_div):
                    ui.icon("leaderboard").classes("text-5xl absolute text-slate-100")
                with ui.element("div").classes(nav_bar_label_div):
                    ui.label("Mini-League").classes("text-slate-100")
        nav_2.on("click", lambda: ui.open(page_creation.by_mini_league_page))

        with ui.element("div").classes(nav_bar_hover_div) as nav_3:
            with ui.element("div").classes(nav_bar_link_div):
                with ui.element("div").classes(nav_bar_icon_div):
                    ui.icon("looks_5").classes("text-5xl absolute text-slate-100")
                with ui.element("div").classes(nav_bar_label_div):
                    ui.label("Top 5").classes("text-slate-100")
        nav_3.on("click", lambda: ui.open(page_creation.by_top_5_page))


@contextmanager
def display():
    with ui.element("div").classes("w-full h-full left-0 top-0 absolute"):
        nav_bar()

        yield
