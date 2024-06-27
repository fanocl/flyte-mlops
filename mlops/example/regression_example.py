import mlflow
from mlops.utils.settings import *
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor

mlflow.set_tracking_uri("{mlflow_fqdn}")

def single_example() -> None:
    # set the experiment id
    mlflow.set_experiment(experiment_id="0")

    mlflow.autolog()
    db = load_diabetes()

    X_train, X_test, y_train, y_test = train_test_split(db.data, db.target)

    # Create and train models.
    rf = RandomForestRegressor(n_estimators=50, max_depth=6, max_features=3)
    rf.fit(X_train, y_train)

    # Use the model to make predictions on the test dataset.
    predictions = rf.predict(X_test)


def nested_example() -> None:
    from mlflow.tracking import MlflowClient
    from mlflow.utils.mlflow_tags import MLFLOW_PARENT_RUN_ID

    client = MlflowClient()
    try:
        experiment = client.create_experiment("Default")
    except:
        experiment = client.get_experiment_by_name("Default").experiment_id
    parent_run = client.create_run(experiment_id=experiment)
    client.log_param(parent_run.info.run_id, "who", "parent")

    child_run_1 = client.create_run(
        experiment_id=experiment,
        tags={
            MLFLOW_PARENT_RUN_ID: parent_run.info.run_id
        }
    )
    client.log_param(child_run_1.info.run_id, "who", "child 1")
    client.log_metric(child_run_1.info.run_id, "R2", 0.8)

    child_run_2 = client.create_run(
        experiment_id=experiment,
        tags={
            MLFLOW_PARENT_RUN_ID: parent_run.info.run_id
        }
    )
    client.log_param(child_run_2.info.run_id, "who", "child 2")
    client.log_metric(child_run_2.info.run_id, "R2", 0.7)

if __name__ == "__main__":
    single_example()
    # nested_example()