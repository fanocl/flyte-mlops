from dotenv import load_dotenv
import mlflow
from mlflow.pyfunc import PyFuncModel
from mlops.utils.settings import MLFLOW_TRACKING_URI

load_dotenv()


class ModelValidation:
    def __init__(self, model_name: str,
                 mlflow_tracking_uri: str = MLFLOW_TRACKING_URI):
        self.model_name = model_name

        # you can set your tracking server URI programmatically:
        mlflow.set_tracking_uri(mlflow_tracking_uri)

        self.client = mlflow.MlflowClient()

    def _load_model(self, alias) -> PyFuncModel:
        # Load model as a PyFuncModel.
        try:
            model = mlflow.pyfunc.load_model(model_uri=f"models:/{self.model_name}@{alias}")
        except Exception as ex:
            print("An error occurred (404) when calling the HeadObject operation: Not Found")
            raise ex

        return model

    def compare_models(self, candidate_model, challenger_model):
        candidate_model = self._load_model(alias='candidate')
        challenger_model = self._load_model(alias='challenger')

        
        # TODO: Required to be upated on latest MLFLOW version
        if self.ml_task == 'Regression':
            best_run_id = child_runs.loc[child_runs['metrics.R2'].idxmax()]['run_id']

    def promote_model(self, version, alias='candidate') -> None:
        self.assign_alias_to_model(version, alias=alias)
        self.assign_tag_to_model(version)

    def assign_alias_to_model(self, version, alias) -> None:
        self.client.set_registered_model_alias(name=self.model_name, alias=alias, version=version)

    def assign_tag_to_model(self, version) -> None:
        self.client.set_model_version_tag(name=self.model_name, version=version, key="validation_status",
                                          value="pending")
