#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Callable, List
import requests
from nicegui import ui,Tailwind,app
import pandas as pd
from typing import Self
import asyncio

from squad_display import show_squad
from search import mini_league_search_bar


def show_page():
    mini_league_search_bar()
