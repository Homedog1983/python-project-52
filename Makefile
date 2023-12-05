install:
	poetry install
lint:
	poetry run flake8 task_manager
dev:
	python3 manage.py runserver
