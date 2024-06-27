import unittest
import mlflow
from mlops.utils.settings import MLFLOW_TRACKING_URI


class MLflowConnectionTest(unittest.TestCase):
    def test_mlflow_server_connection(self):
        try:
            mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
            mlflow.set_experiment("test_mlflow")

            mlflow.start_run()
            mlflow.log_param("test_param", "test_value")
            mlflow.log_metric("test_metric", 0.5)
            mlflow.end_run()

            experiment = mlflow.get_experiment_by_name("test_mlflow")

            self.assertIsNotNone(experiment, "Experiment not found")

        except Exception as e:
            self.fail(f"Failed to connect to MLflow server: {str(e)}")

if __name__ == "__main__":
    unittest.main()
