install:
	poetry install
lint:
	poetry run flake8 task_manager
dev:
	python3 manage.py runserver
PORT ?= 8000
start:
	poetry run python -m gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager:application