import pandas as pd
from flytekit import task
from mlops.workflows import config as cfg


@task(pod_template=cfg.pod_template)
def inference(
        data: pd.DataFrame,
        model_name: str,
        target: str,
        alias: str = 'champion') -> pd.DataFrame:

    import sys
    import os
    wd = '/root/mlops/'
    sys.path.append(wd)
    os.chdir(wd)

    from mlops.model.inference import Inference
    from mlops.utils.settings import MLFLOW_TRACKING_URI

    inf = Inference(data=data,
                    model_name=model_name,
                    target=target,
                    alias=alias,
                    mlflow_tracking_uri=MLFLOW_TRACKING_URI)

    predicted_data = inf.predict()

    return predicted_data