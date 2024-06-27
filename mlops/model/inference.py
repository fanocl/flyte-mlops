import os
from dotenv import load_dotenv
import pandas as pd
import mlflow
from mlflow.pyfunc import PyFuncModel

from mlops.utils.settings import MLFLOW_TRACKING_URI

load_dotenv()


class Inference:
    def __init__(self,
                 data: pd.DataFrame,
                 model_name: str,
                 target: str,
                 alias: str = 'champion',
                 mlflow_tracking_uri=MLFLOW_TRACKING_URI):
        self.data = data
        self.model_name = model_name
        self.target = target
        self.alias = alias

        # you can set your tracking server URI programmatically:
        mlflow.set_tracking_uri(mlflow_tracking_uri)

    def _load_model(self) -> PyFuncModel:
        """
        Load model from mlflow.

        :return: PyFuncModel object.
        :example:
            >>> model = _load_model()
        """

        # Load model as a PyFuncModel.
        try:
            model = mlflow.pyfunc.load_model(model_uri=f"models:/{self.model_name}@{self.alias}")
        except Exception as ex:
            print("An error occurred (404) when calling the HeadObject operation: Model not Found")
            raise ex

        return model

    def predict(self) -> pd.DataFrame:
        """
        Generate predictions.

        :return: pd.DataFrame with predictions.
        :example:
            >>> inference = Inference(data=pd.read_parquet("mlops/test_data/diamond.parquet"),
            >>>                       model_name='diamond_model',
            >>>                       target='Price',
            >>>                       alias='candidate')
            >>> predictions = inference.predict()
        """

        # Get model
        model = self._load_model()

        # Drop target from data
        new_data = self.data.copy().drop(self.target, axis=1)

        # Generate predictions
        predictions = model.predict(new_data)

        # data_final = pd.concat([new_data, pd.DataFrame(predictions)])

        return pd.DataFrame(predictions)
