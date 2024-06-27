ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-slim-buster

WORKDIR /root
ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root

RUN apt-get update && apt-get install -y build-essential

ENV VENV /opt/venv
# Virtual environment
RUN python3 -m venv ${VENV}
ENV PATH="${VENV}/bin:$PATH"

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN python -m pip install poetry
RUN poetry export --without-hashes --with flyte --with mlflow --with inference --without dev -f requirements.txt -o requirements.txt 

RUN pip install -r requirements.txt

COPY /mlops/model/ /root/mlops/model/
COPY /mlops/utils/ /root/mlops/utils/
COPY /mlops/test_data/ /root/mlops/test_data/

RUN rm -rf /root/.env
