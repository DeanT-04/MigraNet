# Makefile for MigraNet

.PHONY: help install test lint format clean docker-build docker-run

# Default target
help:
	@echo "MigraNet - Project Commands"
	@echo "==========================="
	@echo "make install      : Install dependencies"
	@echo "make test         : Run tests with coverage"
	@echo "make lint         : Check code style (flake8)"
	@echo "make format       : Format code (black)"
	@echo "make type-check   : Run static type checking (mypy)"
	@echo "make clean        : Remove build artifacts and cache"
	@echo "make docker-build : Build Docker image"
	@echo "make docker-run   : Run application in Docker"
	@echo "make run          : Run the main analysis script"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

test:
	pytest --cov=english_version/scripts --cov-report=term-missing

lint:
	flake8 .

format:
	black .
	isort .

type-check:
	mypy .

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

docker-build:
	docker build -t migranet .

docker-run:
	docker-compose up app

run:
	python english_version/scripts/main.py
