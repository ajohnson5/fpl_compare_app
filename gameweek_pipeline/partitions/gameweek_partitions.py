from dagster import DynamicPartitionsDefinition

gameweek_partitions_def = DynamicPartitionsDefinition(name="gameweek_partitions_def")
