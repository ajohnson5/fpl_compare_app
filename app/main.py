import asyncio
from nicegui import ui, Client

from router import Router
from common_format import display
import home
import about
import generate_squad


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

    .side_bar {
        width:100% !important;
    }

    @media only screen and (min-width: 640px) {
        .side_bar{
            width:300px !important;   
        }
        .front{
            font-size: 3.75rem !important;
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

    .q-item__section--main~.q-item__section--side {
        padding:0 !important;
    }
    .q-gutter-sm, .q-gutter-x-sm {
        margin-left: 0px;
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

    @router.add("/generate")
    async def generate_squad_page():
        await generate_squad.show_page()

    display(
        [
            (home_page, "Compare."),
            (generate_squad_page, "Generate."),
            (about_page, "About."),
        ],
        router,
    )

    router.frame().classes("w-full")


logo_svg = """
<svg width="81.960785px" height="50.133762px" viewBox="0 0 81.960785 50.133762" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <path d="M38.9999 42.5237C43.5446 47.2166 49.912 50.1338 56.9608 50.1338C70.7679 50.1338 81.9608 38.9409 81.9608 25.1338C81.9608 11.3266 70.7679 0.133766 56.9608 0.133766C50.0993 0.133766 43.8835 2.89796 39.3661 7.37353C43.7235 11.8731 46.4052 18.0051 46.4052 24.7634C46.4052 31.7091 43.5728 37.9932 38.9999 42.5237Z" id="path_1" />
    <clipPath id="clip_1">
      <use xlink:href="#path_1" />
    </clipPath>
  </defs>
  <path d="M48.1791 15.635C43.0153 2.85386 28.4158 -3.34293 15.635 1.82087C2.85401 6.98467 -3.34295 21.5838 1.82085 34.3651C5.74913 44.0882 15.1362 50.0008 25.0311 50.0001C28.1432 49.9998 31.307 49.4148 34.3651 48.1792C47.1461 43.0154 53.343 28.4161 48.1791 15.635L48.1791 15.635ZM36.4172 37.1059L31.8273 32.2493L34.4152 24.2844L40.7991 20.568L45.6981 26.3591C45.509 29.1692 44.7482 31.9017 43.4874 34.3883L36.4172 37.1059L36.4172 37.1059ZM13.5829 37.1059L6.49961 34.3831C6.23504 33.8606 5.98938 33.3237 5.76603 32.771C4.91706 30.6695 4.43949 28.5089 4.29985 26.3616L9.20102 20.568L15.5847 24.2844L18.1726 32.2493L13.5829 37.1059L13.5829 37.1059ZM16.52 6.0693L23.3725 8.67035L23.3725 16.5057L16.8422 21.2501L10.4783 17.5452L10.4783 10.1874C12.1887 8.50631 14.2171 7.0996 16.52 6.0693L16.52 6.0693ZM39.5216 10.1884L39.5216 17.5453L33.1575 21.2502L26.6274 16.5057L26.6274 8.67019L33.4677 6.07383C35.6968 7.07067 37.7521 8.45847 39.5216 10.1884L39.5216 10.1884ZM7.22332 17.866L4.67722 20.8756C5.15027 18.5632 6.01298 16.3458 7.22332 14.3248L7.22332 17.866L7.22332 17.866ZM21.2015 31.0375L18.8537 23.812L25 19.3464L31.146 23.812L28.7984 31.0375L21.2015 31.0375L21.2015 31.0375ZM45.3342 20.889L42.7767 17.866L42.7767 14.3057C43.3301 15.2266 43.8192 16.2018 44.2342 17.2289C44.721 18.4339 45.0848 19.6586 45.3342 20.889L45.3342 20.889ZM28.3532 4.53347L25 5.80635L21.6348 4.5291C23.8922 4.15755 26.1597 4.17048 28.3532 4.53347L28.3532 4.53347ZM9.83261 39.1515L12.9219 40.339L14.4959 42.8775C12.7839 41.8742 11.2094 40.6238 9.83261 39.1515L9.83261 39.1515ZM19.6657 45.0382L16.0602 39.2234L20.72 34.2925L29.2799 34.2925L33.9397 39.2234L30.3271 45.0495C26.7473 46.0035 23.0796 45.9513 19.6657 45.0382L19.6657 45.0382ZM35.4927 42.8958L37.0782 40.3388L40.1629 39.1531C38.8184 40.5979 37.2538 41.8647 35.4927 42.8958L35.4927 42.8958Z" id="Shape" fill="#F5F5F4" fill-rule="evenodd" stroke="none" />
  <g id="Oval-3-Subtract">
    <g clip-path="url(#clip_1)">
      <use xlink:href="#path_1" fill="none" stroke="#F5F5F4" stroke-width="8" />
    </g>
  </g>
</svg>
"""


ui.run(uvicorn_reload_excludes="env", title="FPL Compare", favicon=logo_svg)
