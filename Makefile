.PHONY: run-app
run-app:
	@python3 predict_service.py

.PHONY: run-server
run-server:
	@hypercorn --bind 0.0.0.0:8000 predict_service:app