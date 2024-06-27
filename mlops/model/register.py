from dotenv import load_dotenv
import mlflow
from mlflow import MlflowClient
import pandas as pd

from mlops.utils.settings import MLFLOW_TRACKING_URI

load_dotenv()


class ModelRegister:
    """
    ModelRegister class handles registering ML models with MLflow.

    It takes in a model run ID, model name, and ML task as initialization 
    parameters.
    """
    def __init__(self,
                 model_run_id: str,
                 model_name: str,
                 ml_task: str,
                 mlflow_tracking_uri: str = MLFLOW_TRACKING_URI):

        self.model_run_id = model_run_id
        self.model_name = model_name
        self.ml_task = ml_task

        # you can set your tracking server URI programmatically:
        mlflow.set_tracking_uri(mlflow_tracking_uri)

        self.client = MlflowClient()

    def _get_experiment_name(self) -> str:
        """
        Fetch the experiment name from MLflow with the given run ID.

        :return: The experiment name as a string
        """
        return self.client.get_run(self.model_run_id).data.params['Experiment Name']

    def _get_runs_from_parent(self, run_id: str) -> pd.DataFrame:
        """
        Fetch runs from MLflow with the given parent run ID tag.

        :param run_id (str): The run ID of the parent run
        :return: A DataFrame containing the child runs
        """
        return mlflow.search_runs(experiment_names=[self._get_experiment_name()],
                                       filter_string=f"tags.mlflow.parentRunId='{self.model_run_id}'")

    def _get_best_model_run_id(self, child_runs: pd.DataFrame) -> str:
        """
        Fetch the best model run ID from the given DataFrame of child runs.

        :param child_runs (pd.DataFrame): A DataFrame containing the child runs
        :return: The best model run ID as a string
        """
        if self.ml_task == 'Regression':
            best_run_id = child_runs.loc[child_runs['metrics.R2'].idxmax()]['run_id']

        return best_run_id

    def register_model(self) -> str:
        """
        Register the model with MLflow.

        :return: The version number of the registered model
        """

        # Get parent run id if runs was nested
        child_runs = self._get_runs_from_parent(run_id=self.model_run_id)

        if len(child_runs) == 0:
            best_run_id = self.model_run_id
        else:
            best_run_id = self._get_best_model_run_id(child_runs=child_runs)
   
        # register in model registry
        model_uri = f"runs:/{best_run_id}/model"
        mv = mlflow.register_model(model_uri, self.model_name)
        return mv.version, best_run_id


