from common_format import display
import page_creation
import asyncio
from nicegui import ui
from fastapi import FastAPI

app = FastAPI()

page_creation.create(app)
