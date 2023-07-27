from dagster import (
    sensor,
    AssetSelection,
    RunRequest,
    SkipReason,
    DefaultSensorStatus,
)
import requests


def check_gameweek(gw):
    """Returns true is new gameweek data is ready and false otherwise"""
    url = f"https://fantasy.premierleague.com/api/event/{gw}/live/"
    req = requests.get(url).json()
    if req["elements"]:
        return True
    return False


def make_gameweek_sensor(job):
    @sensor(
        job=job,
        minimum_interval_seconds=3600,
        default_status=DefaultSensorStatus.RUNNING,
    )
    def gameweek_sensor(context):
        """
        Sensor checks to see if gameweek has been completed and adds dynamic partition
        for that gameweek and then materializes all assets with that partition key.

        Args:
            context (OpExecutionContext): object provides system information
            such as resources, config and partitions

        Returns:
            SkipRequest: If gameweek is not finished a SkipRequest is returned so assets
            are not materialized
            RunRequest: If gameweek is completed then assets are materialized for newly
            added partition
        """

        partition_key = context.cursor or "1"
        if not check_gameweek(partition_key):
            return SkipReason("Current gameweek is not completed")

        context.instance.add_dynamic_partitions(
            "gameweek_partitions_def", [partition_key]
        )
        run_request = RunRequest(
            run_key=partition_key, run_config={}, partition_key=partition_key
        )
        # Increment cursor by one
        context.update_cursor(str(int(partition_key) + 1))
        return run_request

    return gameweek_sensor
