profile=mlops

.PHONY: init-env
init-env:
	@poetry shell

.PHONY: run-training
run-training: 
	@poetry run python model_training.py

.PHONY: aws-login
aws-login:
	@aws sso login --sso-session ${profile}

.PHONY: run-server-local
run-server-local:
	@poetry run hypercorn --bind 0.0.0.0:8000 app/predict_service:app

.PHONY: build-image
build-image:
	@docker build -t star-test .

.PHONY: run-server
run-server-docker:
	@docker run -it --rm -p 8000:8000 star-test

.PHONY: aws-deploy
aws-deploy:
	@eb create --timeout 25 --instance-types "t3.small"  star-prediction-env

.PHONY: aws-delete-env
	@eb terminate star-prediction-env