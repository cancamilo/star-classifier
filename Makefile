profile=mlops

.PHONY: aws-login
aws-login:
	@aws sso login --sso-session ${profile}

.PHONY: run-app
run-app:
	@python3 predict_service.py

.PHONY: run-server-local
run-server-local:
	@hypercorn --bind 0.0.0.0:8000 predict_service:app

.PHONY: build-image
build-image:
	@docker build -t star-test .

.PHONY: run-server
run-server:
	@docker run -it --rm -p 8000:8000 star-test