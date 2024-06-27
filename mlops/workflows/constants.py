import os
from dotenv import load_dotenv
load_dotenv()

FLYTE_PROJECT = 'mlops'
FLYTE_DOMAIN = os.getenv('FLYTE_DOMAIN', default="development")

CONTAINER_IMAGE = os.getenv('CONTAINER_IMAGE', default="")

# This should only be changed if the folder structure is changed
GET_TEST_DATA_NAME = 'mlops.workflows.model.reader.get_test_data'

TRAIN_MODEL_NAME = 'dnai.workflows.automl.regression.train_model'
TRAIN_MODEL_VERSION = os.getenv('MLOPS_DNAI_VERSION', default='JPyszDTGzTGxuZNMURHJag')

REGISTER_PROMOTION_NAME = 'mlops.workflows.model.process.register_promotion'

INFERENCE_NAME = 'mlops.workflows.model.inference.inference'