import asyncio
from nicegui import ui, Client

from router import Router
from common_format import display
import home
import about


@ui.page("/")  # normal index page (e.g. the entry point of the app)
@ui.page(
    "/{_:path}"
)  # all other pages will be handled by the router but must be registered
# to also show the SPA index page
async def main(client: Client):
    ui.add_head_html(
        """
    <link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet">
        <style>
    body {
        max-width: 100%;
        padding:0;
        margin:0;
        overflow-x:hidden;
    }
    .input_class.q-field--outlined .q-field__control {
    border-top-left-radius:9999px;
    border-bottom-left-radius:9999px;
    border-top-right-radius:0px;
    border-bottom-right-radius:0px;
    }
    .gw_select_class.q-field--outlined .q-field__control {
    border-top-left-radius:0px;
    border-bottom-left-radius:0px;
    border-top-right-radius:9999px;
    border-bottom-right-radius:9999px;

    }
    .gw_select_class.q-field--outlined .q-field__control {
    padding: 0 2px;
    }
    .gw_select_class.q-field__after, .q-field__append {
    padding-left: 4px;
    }
    .manager_select_class.q-field--outlined .q-field__control {
    border-top-left-radius:0px;
    border-bottom-left-radius:0px;
    border-top-right-radius:0px;
    border-bottom-right-radius:0px;
    }

    .q-field__label {
            font-size:14px
    }

    @media only screen and (min-width: 40em) {
        .q-field__label {
            font-size:16px
        }
        .gw_select_class.q-field--outlined .q-field__control {
            padding: 0 8px;
            }

        .gw_select_class.q-field__after, .q-field__append {
            padding-left: 12px;
        }
    }
    .q-toggle__inner--truthy .q-toggle__thumb {
    left: 0.85em;
    }
    .q-toggle__inner {
    width: 1.6em;
    }
    .q-toggle__track {
    height: 0.5em;
    border-radius: 0.4em;
    }
    .q-toggle__thumb {
    top: 0.375em;
    left: 0.35em;
    width: 0.4em;
    height: 0.4em;
    }
    .q-toggle__thumb .q-icon {
        margin-right:1px;
    }
    .compare_button_class.text-white {
    color: transparent;
    }

    .compare_button_class.q-btn{
    min-height:auto;
    padding: 10px 8px 20px 8px;
    text-transform:none;
    } 

    .side_bar {
        width:100% !important;
    }

    @media only screen and (min-width: 640px) {
        .side_bar{
            width:300px !important;   
        }
    }
    .q-img__content>div {
        padding:0 !important;
    }
    .expansion-element .q-item__section--side>.q-icon{
    font-size: 60px;
    }
    .expansion-element .q-item__section--main~.q-item__section--side {
    align-items: center;
    width: 100%;
    }
    .expansion-element .q-item__section--main {
    width: 0px;
    min-width: 0;
    max-width: 0%;
    }


    .player-card-height {
        height:80px !important;
    }

    @media only screen and (min-width: 400px) {
        .player-card-height {
            height:90px !important;
        }       
    }

    @media only screen and (min-width: 415px) {
        .player-card-height {
            height:95px !important;
        }       
    }

    @media only screen and (min-width: 490px) {
        .player-card-height {
            height:100px !important;
        }
    }
    .pushable {
        position: relative;
        border: none;
        background: transparent;
        padding: 0;
        cursor: pointer;
        outline-offset: 4px;
        transition: filter 250ms;
    }
    .shadow {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 15px;
        border-bottom-right-radius: 0.375rem; 
        border-bottom-left-radius: 0.375rem; 
        background: hsl(0deg 0% 0% / 0.25);
        will-change: transform;
        transform: translateY(2px);
        transition:
        transform
        600ms
        cubic-bezier(.3, .7, .4, 1);
    }
    .edge {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 10px;
        border-bottom-right-radius: 0.375rem; 
        border-bottom-left-radius: 0.375rem; 
        background: linear-gradient(
        to left,
        #a8a29e 0%,
        #d6d3d1 8%,
        #d6d3d1 92%,
        #a8a29e 100%
        );
    }
    .front {
        display: block;
        position: relative;
        padding: 0px 10px 5px 10px;
        border-radius: 6px;
        font-size: 3rem;
        font-weight: 700;
        will-change: transform;
        transform: translateY(-4px);
        transition:
        transform
        600ms
        cubic-bezier(.3, .7, .4, 1);
        background-color: white;
        mix-blend-mode: lighten;
        color:#0ea5e9;
        font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 
        "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, 
        "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
    }
    .pushable:hover {
        filter: brightness(110%);
    }
    .pushable:hover .front {
        transform: translateY(-6px);
        transition:
        transform
        250ms
        cubic-bezier(.3, .7, .4, 1.5);
    }
    .pushable:active .front {
        transform: translateY(-2px);
        transition: transform 34ms;
    }
    .pushable:hover .shadow {
        transform: translateY(4px);
        transition:
        transform
        250ms
        cubic-bezier(.3, .7, .4, 1.5);
    }
    .pushable:active .shadow {
        transform: translateY(1px);
        transition: transform 34ms;
    }
    .pushable:focus:not(:focus-visible) {
        outline: none;
    }

    @media only screen and (min-width: 640px) {
        .front{
            font-size: 3.75rem;
        }
    }

    .q-item__section--main~.q-item__section--side {
        padding:0 !important;
    }
    </style>
    """
    )

    client.content.classes("p-0 m-0").style("--q-primary: #0ea5e9;")
    router = Router()

    @router.add("/")
    async def home_page():
        await home.show_page()

    @router.add("/about")
    async def about_page():
        await about.show_page()

    display(
        [
            (home_page, "Home."),
            (about_page, "About."),
        ],
        router,
    )

    router.frame().classes("w-full")


ui.run(uvicorn_reload_excludes="env")
