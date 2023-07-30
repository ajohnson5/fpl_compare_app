from nicegui import ui
import asyncio

nav_bar_hover_div = (
    "flex flex-row items-center justify-center cursor-pointer w-full "
    "h-[70px] sm:px-4 my-4 hover:bg-stone-200"
)
nav_bar_link_div = "w-full flex flex-row justify-center justify-center"
nav_bar_icon_div = "flex flex-row items-center justify-center sm:justify-end h-full"
nav_bar_label_div = (
    "flex flex-row items-center justify-center content-end "
    "w-full flex-1 border-b-[1px] border-slate-200 hover:border-slate-500 "
)


def nav_bar(nav_links: list, router):
    with ui.element("div").classes("w-screen h-[100px] absolute top-0 left-0"):
        logo = ui.image(
            "https://i.ibb.co/zZV67bx/FPLCOMPARE-stone-100-logo-27-07.png"
        ).classes("w-[175px] absolute top-8 left-6 hover:cursor-pointer")
        logo.on("click", lambda: router.open(nav_links[0][0]))

        menu_state = {"state": True}

        async def overflow_off():
            await ui.run_javascript(
                f"getElement({burger_menu.id}).style.position = 'fixed'"
            )
            await ui.run_javascript(f'getElement({side_bar.id}).className ="side_bar"')

        async def overflow_on():
            await ui.run_javascript(
                f"getElement({burger_menu.id}).style.position = 'absolute'"
            )
            await ui.run_javascript(f'getElement({side_bar.id}).className =""')

        async def menu_open_func():
            menu_state["state"] = not menu_state["state"]
            if menu_state["state"]:
                burger_1.style(
                    "transform: translate(0px, 0px) rotate(0deg);"
                    "background-color:#fafaf9;"
                )
                burger_2.style("opacity:1;transform: translate(0px, 10px)")
                burger_3.style(
                    "transform: translate(0px, 20px) rotate(0deg);"
                    "background-color:#fafaf9;"
                )
                await overflow_on()
            else:
                burger_1.style(
                    "transform: translate(0px, 10px) rotate(45deg);"
                    "background-color:#18181b;"
                )
                burger_2.style("opacity:0; transform: translate(0px, 10px)")
                burger_3.style(
                    "transform: translate(0px, 10px) rotate(-45deg);"
                    "background-color:#18181b;"
                )
                await overflow_off()

        def nav_bar_link(page_link, page_name, router):
            with ui.element("div").classes(nav_bar_hover_div) as menu_link:
                with ui.element("div").classes(nav_bar_link_div):
                    ui.label(page_name).classes(
                        "text-slate-900 text-center text-2xl font-semibold font-sans"
                    )

            menu_link.on("click", lambda: link_select(router, page_link))

        async def link_select(router, page_link):
            router.open(page_link)
            await menu_open_func()

        with ui.element("div").classes(
            "w-[40px] h-[40px] absolute top-9 left-[85vw] md:left-[93vw] z-30 "
            "hover:cursor-pointer block"
        ) as burger_menu:
            burger_1 = ui.label().classes(
                "absolute w-[40px] h-1 bg-stone-100 block transform transition "
                "duration-500 ease-in-out"
            )
            burger_2 = (
                ui.label()
                .classes(
                    "absolute w-[40px] h-1 bg-stone-100 block transform transition "
                    "duration-500 ease-in-out "
                )
                .style("transform: translate(0px, 10px)")
            )
            burger_3 = (
                ui.label()
                .classes(
                    "absolute w-[40px] h-1 bg-stone-100 block transform transition "
                    "duration-500 ease-in-out"
                )
                .style("transform: translate(0px, 20px)")
            )

        with ui.element("div").style(
            "height: 100vh;width: 0;position: fixed; "
            "z-index: 20;top: 0;right: 0;background-color:white; overflow: hidden; "
            "transition: 0.5s;transition-timing-function:cubic-bezier(0.4, 0, 0.2, 1); "
            "padding-top: 100px;text-align:center;filter: "
            "drop-shadow(0 20px 13px rgb(0 0 0 / 0.03)) "
            "drop-shadow(0 8px 5px rgb(0 0 0 / 0.08));"
        ).classes("drop-shadow-xl") as side_bar:
            for link in nav_links:
                nav_bar_link(link[0], link[1], router)

            with ui.link(target="https://github.com/ajohnson5"):
                ui.element("i").classes("eva eva-github").classes(
                    "text-5xl hover:scale-105 hover:cursor-pointer pt-4 text-zinc-900"
                )

    burger_menu.on("click", lambda x: menu_open_func())


def display(nav_links: list, router):
    ui.element("div").classes(
        (
            "h-screen w-screen bg-gradient-to-b from-sky-500 via-sky-300 to-cyan-100 "
            "absolute top-0 left-0 -z-10"
        )
    )
    nav_bar(nav_links, router)
    return
