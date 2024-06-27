import os
from dotenv import load_dotenv
load_dotenv()

APP_NAME = os.getenv('APP_NAME', default='mlops')
"""The name of the application (`str`).

Used more for logging purposes.
"""

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', default="")
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', default="")

MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI', default='http://localhost:5000')

MLFLOW_TRACKING_INSECURE_TLS = os.getenv('MLFLOW_TRACKING_INSECURE_TLS', default='false')
MLFLOW_TRACKING_SERVER_CERT_PATH = os.getenv('MLFLOW_TRACKING_SERVER_CERT_PATH', default='')
MLFLOW_S3_ENDPOINT_URL = os.getenv('MLFLOW_S3_ENDPOINT_URL', default='')