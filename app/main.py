import asyncio
from nicegui import ui, Client

from common_format import display
import home


@ui.page("/")  # normal index page (e.g. the entry point of the app)
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

    .q-field__control {
        background: #fafaf9;
    }

    .input_class.q-field--outlined .q-field__control {
        border-top-left-radius:0px;
        border-bottom-left-radius:0px;
        border-top-right-radius:0px;
        border-bottom-right-radius:0px;
    }

    .manager_1_input_class.q-field--outlined .q-field__control {
        border-top-right-radius:25px;
        border-color: #0ea5e9 !important; 
    }
    .manager_2_input_class.q-field--outlined .q-field__control {
        border-bottom-left-radius:25px;
        border-color: #ef4444 !important; 
    }


    .gw_select_class.q-field--outlined .q-field__control {
    border-top-left-radius:0px;
    border-bottom-left-radius:0px;
    border-top-right-radius:0px;
    border-bottom-right-radius:0px;
    }
    .update_league_id_input_radius.q-field--outlined .q-field__control {
        border-top-right-radius:0px;
    }

    .update_manager_select_radius.q-field--outlined .q-field__control {
        border-top-right-radius:25px !important;
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

    .manager_1_input_class .q-checkbox__inner--truthy {
        color: #0ea5e9; 
    }

    .manager_2_input_class .q-checkbox__inner--truthy {
        color: #ef4444; 
    }

    .gameweek_button.q-btn--rectangle {
        border-top-left-radius: 0px;
        border-bottom-left-radius: 0px;
        border-top-right-radius: 25px;
        border-bottom-right-radius: 25px;
    }


    .gameweek_button.q-btn {
        font-weight:800;
        font-size: 1.5em;
        line-height: 2em;
        padding: 3px 8px 3px 3px;
        min-height: initial;

    }

    .gameweek_1.q-btn {
        color: #0ea5e9; 
    }

    .gameweek_2.q-btn {
        color: #ef4444; 
    }

    .gameweek_button.q-btn:before {
        box-shadow: none;
    }

    .set_manager_1_button.q-btn {
        background: linear-gradient(to right, rgb(14, 165, 233), rgb(147, 197, 253), rgb(34, 211, 238)) !important;
    }

    .set_manager_2_button.q-btn {
        background:linear-gradient(to right, rgb(239, 68, 68), rgb(248, 113, 113), rgb(251, 113, 133)) !important;
    }

    .return_button_class .on-left {
        margin-right:0px
    }

    .q-field__native > span {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
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

    .q-carousel__control.flex-center {
        align-items: end;
    }
    .q-field__inner.self-stretch {
    align-self:center;
    }

    .q-item {
        align-items:center;
        justify-content:center;
        padding:0;
    }

    .rect {
    height: 100px;
    width: 100px;
    background: rgba(0, 0, 0, 0.5);
    position: relative;
    margin-top: 100px;
    margin-left: 100px;
    }

    .circle {
    display: block;
    width: 100px;
    height: 50px;
    top: -50px;
    left: 0;
    overflow: hidden;
    position: absolute;
    }

    .circle::after {
    content: '';
    width: 100px;
    height: 100px;
    -moz-border-radius: 100px;
    -webkit-border-radius: 100px;
    border-radius: 100px;
    background: rgba(0, 0, 0, 0);
    position: absolute;
    top: -100px;
    left: -40px;
    border: 40px solid rgba(0, 0, 0, 0.5);
    }

    </style>
    """
    )

    client.content.classes("p-0 m-0").style("--q-primary: #0ea5e9;")

    
    await home.show_page()



logo_svg = """
<svg
   width="50.192448mm"
   height="30.000233mm"
   viewBox="0 0 50.192449 30.000232"
   version="1.1"
   id="svg1"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <defs
     id="defs1">
    <rect
       x="293.86978"
       y="748.83093"
       width="1190.4094"
       height="419.40659"
       id="rect43" />
    <linearGradient
       id="swatch34">
      <stop
         style="stop-color:#000000;stop-opacity:1;"
         offset="0"
         id="stop34" />
    </linearGradient>
  </defs>
  <g
     id="layer1"
     transform="translate(-41.719131,-85.566433)">
    <g
       id="g47"
       transform="translate(-41.456701,-87.675276)"
       style="fill:#44403c;fill-opacity:1">
      <g
         id="g42"
         transform="matrix(1.0390447,0,0,1.0516628,63.147513,90.181313)"
         style="fill:#44403c;fill-opacity:1">
        <path
           id="path1"
           style="fill:#44403c;fill-opacity:1;stroke-width:0.313088"
           d="M 53.145595,78.980065 A 14.436337,14.263127 0 0 0 38.709144,93.243304 14.436337,14.263127 0 0 0 53.145595,107.50654 14.436337,14.263127 0 0 0 67.582042,93.243304 14.436337,14.263127 0 0 0 53.145595,78.980065 Z m 0,4.754577 a 9.6242247,9.5087509 0 0 1 9.624137,9.508662 9.6242247,9.5087509 0 0 1 -9.624137,9.508666 9.6242247,9.5087509 0 0 1 -9.624134,-9.508666 9.6242247,9.5087509 0 0 1 9.624134,-9.508662 z" />
        <path
           id="path1-8"
           style="fill:#44403c;fill-opacity:1;stroke-width:0.313826"
           d="m 32.987102,78.995802 c -3.863572,0.192817 -7.487545,1.916814 -10.059313,4.785418 -4.869447,5.431565 -4.869447,13.622228 0,19.05379 4.86945,5.43153 13.31342,6.16637 19.313359,1.99583 l -3.019819,-3.71291 c -1.612894,1.12807 -3.536085,1.73679 -5.509098,1.74374 -5.315436,2.3e-4 -9.624582,-4.277098 -9.624632,-9.553554 4.9e-5,-5.276456 4.309195,-9.553779 9.624632,-9.553556 1.974794,0.0011 3.90144,0.605246 5.518547,1.730413 l 3.377037,-3.741018 c -2.62999,-1.828078 -6.414113,-2.908202 -9.620713,-2.748153 z" />
      </g>
      <text
         xml:space="preserve"
         transform="matrix(0.08178538,0,0,0.08336071,38.875327,158.38144)"
         id="text43"
         style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:205.08px;font-family:Bahnschrift;-inkscape-font-specification:Bahnschrift;white-space:pre;shape-inside:url(#rect43);fill:#44403c;fill-opacity:1;fill-rule:nonzero" />
    </g>
  </g>
</svg>
"""


ui.run(uvicorn_reload_excludes="env", title="FPL Compare", favicon=logo_svg)
