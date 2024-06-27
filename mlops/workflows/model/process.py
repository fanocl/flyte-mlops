from flytekit import task
from typing import Dict
from mlops.workflows import config as cfg


@task(pod_template=cfg.pod_template)
def register_promotion(
        model_run_id: str,
        model_name: str,
        ml_task: str) -> str:

    import sys
    import os
    wd = '/root/mlops/'
    sys.path.append(wd)
    os.chdir(wd)

    from mlops.model.register import ModelRegister
    from mlops.model.promotion import ModelPromotion
    from mlops.utils.settings import MLFLOW_TRACKING_URI

    mr = ModelRegister(model_run_id=model_run_id,
                       model_name=model_name,
                       ml_task=ml_task,
                       mlflow_tracking_uri=MLFLOW_TRACKING_URI)
    model_version, run_id = mr.register_model()

    mp = ModelPromotion(model_name=model_name,
                        mlflow_tracking_uri=MLFLOW_TRACKING_URI)
    mp.promote_model(version=model_version)

    return model_name

