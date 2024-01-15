from dagster import validate_run_config, define_asset_job, build_sensor_context
from gameweek_pipeline.sensors import make_gameweek_sensor

fpl_asset_job = define_asset_job(name="fpl_asset_job")
gameweek_sensor = make_gameweek_sensor(fpl_asset_job)


def test_gameweek_sensor():
    context = build_sensor_context(cursor="1")
    for run_request in gameweek_sensor(context):
        assert validate_run_config(fpl_asset_job, run_request.run_config)
