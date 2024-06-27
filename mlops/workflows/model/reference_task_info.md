## This is only an example of how a reference task would look like for mlops (if used)


```py
# This should only be changed if the folder structure is changed
GET_TEST_DATA_NAME = 'mlops.workflows.model.reader.get_test_data'

TRAIN_MODEL_NAME = 'dnai.workflows.automl.regression.train_model'

REGISTER_PROMOTION_NAME = 'mlops.workflows.model.process.register_promotion'

INFERENCE_NAME = 'mlops.workflows.model.inference.inference'

@reference_task(
    project=FLYTE_PROJECT,
    domain=FLYTE_DOMAIN,
    name=GET_TEST_DATA_NAME,
    version=version
)
def get_test_data(name: str):
    """
    The empty function acts as a convenient skeleton to make it intuitive to call/reference this task from workflows.
    The interface of the task must match that of the remote task. Otherwise, remote compilation of the workflow will
    fail.

    The remote task is found in the mlops repository.
    """    

@reference_task(
    project=FLYTE_PROJECT,
    domain=FLYTE_DOMAIN,
    name=REGISTER_PROMOTION_NAME,
    version=version
)
def register_promotion(
    model_run_id: str,
    model_name: str,
    ml_task: str
    ):
    """
    The empty function acts as a convenient skeleton to make it intuitive to call/reference this task from workflows.
    The interface of the task must match that of the remote task. Otherwise, remote compilation of the workflow will
    fail.

    The remote task is found in the mlops repository.
    """


@reference_task(
    project=FLYTE_PROJECT,
    domain=FLYTE_DOMAIN,
    name=INFERENCE_NAME,
    version=version
)
def inference(
    data: pd.DataFrame, model_name: str, target: str, alias: str
    ):
    """
    The empty function acts as a convenient skeleton to make it intuitive to call/reference this task from workflows.
    The interface of the task must match that of the remote task. Otherwise, remote compilation of the workflow will
    fail.

    The remote task is found in the mlops repository.
    """
```