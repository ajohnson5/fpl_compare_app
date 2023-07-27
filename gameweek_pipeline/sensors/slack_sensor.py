from dagster import (
    run_status_sensor,
    RunStatusSensorContext,
    DagsterRunStatus,
    run_failure_sensor,
    RunFailureSensorContext,
    DefaultSensorStatus,
)
import os
from slack_sdk import WebClient


@run_status_sensor(
    run_status=DagsterRunStatus.SUCCESS, default_status=DefaultSensorStatus.RUNNING
)
def my_slack_on_run_success(context: RunStatusSensorContext):
    slack_client = WebClient(token=os.environ["SLACK_DAGSTER_ETL_BOT_TOKEN"])

    slack_client.chat_postMessage(
        channel=os.environ["SLACK_CHANNEL"],
        text=f'Job "{context.dagster_run.job_name}" succeeded.',
    )


@run_failure_sensor(default_status=DefaultSensorStatus.RUNNING)
def my_slack_on_run_failure(context: RunFailureSensorContext):
    slack_client = WebClient(token=os.environ["SLACK_DAGSTER_ETL_BOT_TOKEN"])

    slack_client.chat_postMessage(
        channel=os.environ["SLACK_CHANNEL"],
        text=(
            f'Job "{context.dagster_run.job_name}" failed. Error:'
            f" {context.failure_event.message}"
        ),
    )
