from nicegui import ui


def individual_manager_summary(home: bool):
    if home:
        bg_color = " from-sky-500 via-sky-300 to-cyan-400"
    else:
        bg_color = " from-red-500 via-red-400 to-rose-400"
    with ui.element("div").classes(
        " p-1 bg-gradient-to-r rounded-2xl drop-shadow-xl" + bg_color
    ):
        manager_display = ui.element("div").classes(
            " w-[155px] md:w-[250px] flex flex-row justify-center "
            "content-start gap-y-0"
        )

    return manager_display


def manager_summary_layout():
    with ui.element("div").classes(
        "w-full h-auto flex flex-row justify-center content-center mx-2 "
        "gap-x-4 lg:gap-x-[270px] mb-4 gap-y-2"
    ):
        manager_1_display = individual_manager_summary(home=True)
        manager_2_display = individual_manager_summary(home=False)

        return manager_1_display, manager_2_display


def player_icon_key():
    with ui.element("div").classes(
        "flex flex-row justify-center  gap-x-4 gap-y-2 mb-2"
    ):
        with ui.element("div").classes("flex flex-row content-center items-center"):
            ui.icon("copyright", color="zinc-900", size="sm")
            ui.label("Captain").classes("ml-1")
        with ui.element("div").classes("flex flex-row content-center items-center"):
            ui.icon("local_fire_department", color="zinc-900", size="sm")
            ui.label("Triple Captain").classes("ml-1")
        with ui.element("div").classes("flex flex-row content-center items-center"):
            ui.icon("add_circle", color="zinc-900", size="sm")
            ui.label("Auto sub in").classes("ml-1")
        with ui.element("div").classes("flex flex-row content-center items-center"):
            ui.icon("do_not_disturb_on", color="zinc-900", size="sm")
            ui.label("Auto sub out").classes("ml-1 ")
        with ui.element("div").classes("flex flex-row content-center items-center"):
            ui.icon("info", color="zinc-900", size="sm")
            ui.label("Transfer Info").classes("ml-1 ")


def pitch_layout():
    with ui.element("div").classes(
        "mx-[4px] w-full gap-x-10 flex flex-row justify-center content-center mb-4"
    ):
        with ui.element("div").classes(
            "px-2 pt-2 lg:pb-2 w-full max-w-[490px] rounded-t-xl lg:rounded-b-xl "
            "bg-gradient-to-b from-green-400 via-emerald-400 to-emerald-500"
        ):
            with ui.image(
                "https://private-user-images.githubusercontent.com/99501368/258434948-995105cb-e14f-43f7-b12b-af0efa756d3d.svg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTEiLCJleHAiOjE2OTExNTY0NDUsIm5iZiI6MTY5MTE1NjE0NSwicGF0aCI6Ii85OTUwMTM2OC8yNTg0MzQ5NDgtOTk1MTA1Y2ItZTE0Zi00M2Y3LWIxMmItYWYwZWZhNzU2ZDNkLnN2Zz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFJV05KWUFYNENTVkVINTNBJTJGMjAyMzA4MDQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjMwODA0VDEzMzU0NVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWM2YzkwZThmYzhjNjBjOTYzYThlYjk0NjNjMzVlZGQyNzgwYzQ1NTg3ZDJjMDM4NjNjNjU1NzkyNzZkMzg0NWImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.JHLjomLl9dDyrD65YTnghfP592_MIhSsryf9W6A1LWg"
            ).classes("max-w-[482px] w-full"):
                squad_1_display = ui.element("div").classes(
                    "w-full h-full bg-transparent grid-rows-4 grid grid-cols-1 gap-0"
                )

        with ui.element("div").classes(
            "px-2 lg:pt-2 pb-2 w-full max-w-[490px] rounded-b-xl lg:rounded-t-xl "
            "bg-gradient-to-b from-emerald-500 via-emerald-400 to-green-400 "
            "lg:bg-gradient-to-t"
        ):
            with ui.image(
                "https://private-user-images.githubusercontent.com/99501368/258434948-995105cb-e14f-43f7-b12b-af0efa756d3d.svg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTEiLCJleHAiOjE2OTExNTY0NDUsIm5iZiI6MTY5MTE1NjE0NSwicGF0aCI6Ii85OTUwMTM2OC8yNTg0MzQ5NDgtOTk1MTA1Y2ItZTE0Zi00M2Y3LWIxMmItYWYwZWZhNzU2ZDNkLnN2Zz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFJV05KWUFYNENTVkVINTNBJTJGMjAyMzA4MDQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjMwODA0VDEzMzU0NVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWM2YzkwZThmYzhjNjBjOTYzYThlYjk0NjNjMzVlZGQyNzgwYzQ1NTg3ZDJjMDM4NjNjNjU1NzkyNzZkMzg0NWImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.JHLjomLl9dDyrD65YTnghfP592_MIhSsryf9W6A1LWg"
            ).classes("max-w-[482px] w-full rotate-180 lg:rotate-0"):
                squad_2_display = ui.element("div").classes(
                    "w-full h-full bg-transparent grid-rows-4 grid grid-cols-1 gap-0"
                )

    return squad_1_display, squad_2_display


def bench_layout():
    with ui.element("div").classes(
        "w-full  flex flex-row justify-center content-center gap-x-10 mb-4 "
        "mx-2 gap-y-4"
    ):
        with ui.element("div").classes(
            "w-full max-w-[490px] p-1 bg-gradient-to-r rounded-2xl "
            "from-sky-500 via-sky-300 to-cyan-400 drop-shadow-xl "
        ):
            bench_1_display = ui.element("div").classes(
                "w-full max-w-[490px] h-full flex flex-row justify-evenly "
                "bg-slate-50/50 content-center rounded-xl pb-1"
            )

        with ui.element("div").classes(
            "w-full max-w-[490px] p-1 bg-gradient-to-r rounded-2xl "
            "from-red-500 via-red-400 to-rose-400 drop-shadow-xl"
        ):
            bench_2_display = ui.element("div").classes(
                "w-full  max-w-[490px] h-full flex flex-row justify-evenly "
                "bg-slate-50/50 content-center rounded-xl pb-1"
            )
    return bench_1_display, bench_2_display


def transfer_expansion():
    with ui.expansion("", value=True).classes("bg-slate-50/50 rounded-xl").classes(
        "expansion-element"
    ).props(
        'header-class="text-white text-center text-2xl rounded-xl h-[80px]"'
        'expand-icon-class="text-white" expand-icon="keyboard_double_arrow_down"'
    ):
        transfer_display = ui.element("div").classes("col-span-1 h-auto pb-2")
    return transfer_display


def transfer_layout():
    with ui.element("div").classes(
        "mx-[4px] w-full gap-x-10 gap-y-4 flex flex-row justify-center "
        "content-center mb-4 "
    ):
        with ui.element("div").classes("w-full max-w-[490px] h-auto "):
            with ui.element("div").classes(
                "bg-gradient-to-r from-sky-500 via-sky-300 to-cyan-400 p-1 "
                "rounded-2xl w-full mx-auto"
            ):
                transfer_1_display = transfer_expansion()

        with ui.element("div").classes("w-full max-w-[490px]  h-auto "):
            with ui.element("div").classes(
                "bg-gradient-to-r from-red-500 via-red-400 to-rose-400 p-1 "
                "rounded-2xl w-full mx-auto"
            ):
                transfer_2_display = transfer_expansion()
    return transfer_1_display, transfer_2_display


def squad_summary():
    with ui.element("div").classes(
        "p-1 rounded-2xl drop-shadow-xl bg-gradient-to-r from-sky-500 via-sky-300 "
        "to-cyan-400"
    ) as squad_summary_container:
        squad_summary_display = ui.element("div").classes(
            " flex flex-row justify-centers " "content-start gap-y-0"
        )

    return squad_summary_container, squad_summary_display


def generate_squad_pitch_layout():
    with ui.element("div").classes(
        "mx-2 w-full flex flex-row justify-center content-center mb-4"
    ):
        with ui.element("div").classes(
            "px-2 py-2 w-full max-w-[490px] rounded-t-xl lg:rounded-b-xl "
            "bg-gradient-to-b from-green-400 via-emerald-400 to-emerald-500"
        ):
            with ui.image(
                "https://i.ibb.co/xS9j0v0/half-pitch-complete-final-4.png"
            ).classes("max-w-[482px] w-full"):
                squad_display = ui.element("div").classes(
                    "w-full h-full bg-transparent grid-rows-4 grid grid-cols-1 gap-0"
                )

        return squad_display
