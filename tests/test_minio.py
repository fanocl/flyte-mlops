import unittest
import boto3

from mlops.utils.settings import MLFLOW_S3_ENDPOINT_URL, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


class MinioConnectionTest(unittest.TestCase):
    def test_minio_server_connection(self):
        try:
            minio_client = boto3.client(
                "s3",
                endpoint_url=MLFLOW_S3_ENDPOINT_URL,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                verify=False,
            )
            response = minio_client.list_buckets()
            self.assertIsNotNone(response["Buckets"], "No buckets found")

        except Exception as e:
            self.fail(f"Failed to connect to MinIO server: {str(e)}")


if __name__ == "__main__":
    unittest.main()
