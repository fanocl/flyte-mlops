from flytekitplugins.pod import Pod
from flytekit import PodTemplate
from kubernetes.client.models import (
    V1PodSpec,
    V1Container,
    V1VolumeMount,
    V1Volume,
    V1SecretVolumeSource,
    V1EnvVar,
    V1EnvVarSource,
    V1SecretKeySelector,
    V1Toleration,
)

from mlops.workflows.constants import CONTAINER_IMAGE

# TODO: Make part of CI (Not hardcoded)
image = CONTAINER_IMAGE

AWS_SECRET_GROUP = 'aws'
MLFLOW_SECRET_GROUP = 'mlflow'
MLFLOW_CERT_GROUP = 'mlflow-ca-cert'
MLFLOW_TRACKING_USERNAME = 'mlflow.tracking.username'
MLFLOW_TRACKING_PASSWORD = 'mlflow.tracking.password'
MLFLOW_TRACKING_URI = 'mlflow.tracking.uri'
MLFLOW_TRACKING_SERVER_CERT_PATH = 'mlflow.tracking.cacert'
AWS_ACCESS_KEY_ID = 'aws.access.key.id'
AWS_SECRET_ACCESS_KEY = 'aws.secret.access.key'


# The following approach is only because flyte 1.10.6 deployment has a bug where the webhook does not mount the secrets.
secret_requests = {
    "MLFLOW_TRACKING_USERNAME": [MLFLOW_SECRET_GROUP, MLFLOW_TRACKING_USERNAME],
    "MLFLOW_TRACKING_PASSWORD": [MLFLOW_SECRET_GROUP, MLFLOW_TRACKING_PASSWORD],
    "MLFLOW_TRACKING_URI": [MLFLOW_SECRET_GROUP, MLFLOW_TRACKING_URI],
    "MLFLOW_TRACKING_SERVER_CERT_PATH": [MLFLOW_SECRET_GROUP, MLFLOW_TRACKING_SERVER_CERT_PATH],
    # "AWS_ACCESS_KEY_ID": [AWS_SECRET_GROUP, AWS_ACCESS_KEY_ID],
    # "AWS_SECRET_ACCESS_KEY": [AWS_SECRET_GROUP, AWS_SECRET_ACCESS_KEY],
     }

envs = []
for key, values in secret_requests.items():
    envar = V1EnvVar(name=f"{key}",
                     value_from=V1EnvVarSource(secret_key_ref=V1SecretKeySelector(name=values[0],
                                                                                  key=values[1])))
    envs.append(envar)

pod_template = PodTemplate(
    primary_container_name="primary",
    labels={"app": "flyte"},
    annotations={"app": "flyte"},
    pod_spec=V1PodSpec(
        containers=[
            V1Container(
                name='primary',
                image=image,
                env=envs,
                volume_mounts=[
                    V1VolumeMount(mount_path='/etc/ssl/certs', name=MLFLOW_CERT_GROUP)
                ]
            )
        ],
        volumes=[
            V1Volume(name=MLFLOW_CERT_GROUP, secret=V1SecretVolumeSource(secret_name=MLFLOW_CERT_GROUP))
        ],
        # node_selector={"app": "flyte"},
        # tolerations=[
        #     V1Toleration(
        #         key="app",
        #         operator="Equal",
        #         value="flyte",
        #         effect="NoSchedule",
        #     ),
        # ],
    )
)

