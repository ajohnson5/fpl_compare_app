import asyncio
from nicegui import ui, Client

from common_format import display
from layout_components import favicon_logo, css
import home


@ui.page("/")
async def main(client: Client):
    ui.add_head_html(css)

    client.content.classes("p-0 m-0").style("--q-primary: #0ea5e9;")

    await home.show_page()


ui.run(uvicorn_reload_excludes="env", title="FPL Compare", favicon=favicon_logo)
