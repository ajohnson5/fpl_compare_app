from dagster import Definitions
from gameweek_pipeline.assets import players
from gameweek_pipeline.sensors import gameweek_sensor


defos = Definitions(
    assets=[players],
    sensors=[gameweek_sensor],
)
