run-exeperiment:
	python ./mlops/example/regression_example.py

start-server:
	mlflow ui

docker-build:
	docker build --no-cache -t fanoclar/dev-mlops:latest  -f ./Dockerfile .

docker-push:
	docker push fanoclar/dev-mlops:latest

docker-start: docker-build docker-push
	echo "."

ecr:
	aws ecr get-login-password --region af-south-1 | docker login --username AWS --password-stdin <aws_account>.dkr.ecr.af-south-1.amazonaws.com
	docker build -t <aws_account>.dkr.ecr.af-south-1.amazonaws.com/dev-mlops:2.10.2-0.0.1 -f ./Dockerfile . --build-arg PYTHON_VERSION=3.10.8
	docker push <aws_account>.dkr.ecr.af-south-1.amazonaws.com/dev-mlops:2.10.2-0.0.1

register-test:
	pyflyte register "./mlops" --project mlops --domain development --env FLYTE_DOMAIN=development --env CONTAINER_IMAGE=<aws_account>.dkr.ecr.af-south-1.amazonaws.com/dev-mlops:2.10.2-0.0.1 --service-account flytepropeller --dry-run

register-with-env:
	pyflyte register "./mlops" --project mlops --domain development --env FLYTE_DOMAIN=development --env CONTAINER_IMAGE=<aws_account>.dkr.ecr.af-south-1.amazonaws.com/dev-mlops:2.10.2-0.0.1 --service-account flytepropeller

