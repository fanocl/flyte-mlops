import pandas as pd
from flytekit import task
from mlops.workflows import config as cfg

#TODO: Investigate caching this task since the data will be static.

@task(pod_template=cfg.pod_template)
def get_test_data(name: str) -> pd.DataFrame:
    # This is an example. Will require integration with ontology platform

    if name == "diamond":
        data = pd.read_parquet("mlops//test_data//diamond.parquet")

    return data