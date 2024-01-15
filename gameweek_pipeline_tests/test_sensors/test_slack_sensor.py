from dagster import (
    op,
    job,
    DagsterInstance,
    build_run_status_sensor_context,
    validate_run_config,
    define_asset_job,
    build_sensor_context,
)
from gameweek_pipeline.sensors import my_slack_on_run_success, my_slack_on_run_failure


@op
def succeeds():
    return 1


@op
def fails():
    raise Exception("Dummy Failure")


@job
def dummy_job_success():
    succeeds()


@job
def dummy_job_failure():
    fails()


def test_slack_success_sensor():
    # execute the job
    instance = DagsterInstance.ephemeral()
    success_result = dummy_job_success.execute_in_process(instance=instance)

    # failure_result = dummy_job_failure.execute_in_process(instance=instance)

    # retrieve the DagsterRun
    dagster_run = success_result.dagster_run

    # retrieve a success event from the completed execution
    dagster_event = success_result.get_job_success_event()

    # create the context
    run_status_sensor_context = build_run_status_sensor_context(
        sensor_name="my_slack_on_run_success",
        dagster_instance=instance,
        dagster_run=dagster_run,
        dagster_event=dagster_event,
    )

    # run the sensor
    my_slack_on_run_success(run_status_sensor_context)

    # my_slack_on_run_failure(run_status_sensor_context)
