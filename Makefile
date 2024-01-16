install:
	poetry install
lint:
	poetry run flake8 task_manager
dev:
	python3 manage.py runserver
test:
	python manage.py test --noinput -v 2
test-coverage:
	coverage run --source='.' manage.py test
	coverage xml
PORT ?= 8000
start:
	poetry run python -m gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager:application