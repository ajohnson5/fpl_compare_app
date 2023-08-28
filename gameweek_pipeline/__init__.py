from firebase_admin import initialize_app, firestore_async, firestore
from dagster import (
    Definitions,
    define_asset_job,
    ConfigurableResource,
    in_process_executor,
)
from gameweek_pipeline.assets import players, fixtures
from gameweek_pipeline.sensors import (
    make_gameweek_sensor,
    my_slack_on_run_failure,
    my_slack_on_run_success,
)


# Firestore Resource (Batch load data)
class firestoreClient(ConfigurableResource):
    def get_client(
        self,
    ):
        # Initialize app on first call
        # Note you must set GOOGLE_CLOUD_PROJECT in your .env file
        try:
            initialize_app()
        except ValueError:
            print("App already exists")
        finally:
            return firestore.client()

    # Batch function takes ~8 seconds
    def load_batch(self, collection: str, data):
        client = self.get_client()
        batch = client.batch()
        counter = 0
        for key, value in data.items():
            ref = client.collection(collection).document(key)
            batch.set(ref, value, merge=True)
            counter += 1
            if counter == 499:
                batch.commit()
                batch = client.batch()
                counter = 0

        batch.commit()


fpl_asset_job = define_asset_job(name="fpl_asset_job")

gameweek_sensor = make_gameweek_sensor(fpl_asset_job)


defos = Definitions(
    assets=[players, fixtures],
    jobs=[fpl_asset_job],
    sensors=[gameweek_sensor, my_slack_on_run_failure, my_slack_on_run_success],
    resources={"firestore_client": firestoreClient()},
)
