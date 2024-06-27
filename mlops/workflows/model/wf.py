import pandas as pd
from flytekit import workflow, reference_task
from mlops.workflows import config as cfg
from mlops.workflows.constants import (FLYTE_PROJECT,
                                       FLYTE_DOMAIN,
                                       TRAIN_MODEL_NAME,
                                       TRAIN_MODEL_VERSION)



@reference_task(
    project=FLYTE_PROJECT,
    domain=FLYTE_DOMAIN,
    name=TRAIN_MODEL_NAME,
    version=TRAIN_MODEL_VERSION
)
def train_model(data: pd.DataFrame, target: str, experiment_name: str, method: str = 'pycaret') -> str:
    """
    The empty function acts as a convenient skeleton to make it intuitive to call/reference this task from workflows.
    The interface of the task must match that of the remote task. Otherwise, remote compilation of the workflow will
    fail.

    The remote task is found in the mlops-dnai repository.
    """   



from mlops.workflows.model.reader import get_test_data
from mlops.workflows.model.process import register_promotion
from mlops.workflows.model.inference import inference

@workflow()
def test_model_training_pipeline(name: str, target: str, ml_task: str, method: str, experiment_name: str, model_name: str) -> pd.DataFrame:
    data = get_test_data(name=name)
    model_run_id = train_model(data=data, target=target, experiment_name=experiment_name, method=method)
    promoted_model_name = register_promotion(model_run_id=model_run_id, model_name=model_name, ml_task=ml_task)

    predicted_data = inference(data=data, model_name=promoted_model_name, target=target, alias='candidate')
    
    return predicted_data
