# Variables
PROJECT_NAME = map_my_crop
VENV_NAME = .venv
PYTHON = ../$(VENV_NAME)/bin/python
PIP = ../$(VENV_NAME)/bin/pip
UVICORN = ../$(VENV_NAME)/bin/uvicorn
FLAKE8 = ../$(VENV_NAME)/bin/flake8
PYTEST = ../$(VENV_NAME)/bin/pytest

# Targets
.PHONY: setup run test lint format clean

setup:
	@echo "Setting up virtual environment..."
	python3 -m venv ../$(VENV_NAME)
	$(PIP) install -r requirements.txt
	@echo "Setup complete."

run:
	@echo "Starting FastAPI server..."
	$(UVICORN) main:app --reload

test:
	@echo "Running unit tests..."
	$(PYTEST) tests/test.py

lint:
	@echo "Linting code..."
	$(FLAKE8) .

