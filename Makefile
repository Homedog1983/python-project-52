PORT ?= 8000
LGRN='\033[1;32m'
setup: build_dependencies install_project
build_dependencies:
	echo -e "${LGRN}build_dependencies:"
	python -m pip install --upgrade pip
	pip install -r requirements.txt
install_project:
	echo -e "${LGRN}install project:"
	poetry install
	python manage.py collectstatic --no-input
	python manage.py migrate
lint:
	poetry run flake8 task_manager
dev:
	python3 manage.py runserver
test:
	python manage.py test --noinput -v 2
test-coverage:
	coverage run --source='.' manage.py test
	coverage xml
start:
	poetry run python -m gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager:application