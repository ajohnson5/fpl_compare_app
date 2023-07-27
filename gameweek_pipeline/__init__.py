from dagster import Definitions, define_asset_job
from gameweek_pipeline.assets import players
from gameweek_pipeline.sensors import (
    make_gameweek_sensor,
    my_slack_on_run_failure,
    my_slack_on_run_success,
)


fpl_asset_job = define_asset_job(name="fpl_asset_job")

gameweek_sensor = make_gameweek_sensor(fpl_asset_job)


defos = Definitions(
    assets=[players],
    jobs=[fpl_asset_job],
    sensors=[gameweek_sensor, my_slack_on_run_failure, my_slack_on_run_success],
)
