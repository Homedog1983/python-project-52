PORT ?= 8000
LGRN_COLOR='\033[1;32m'
NORM_COLOR='\033[0m'

setup: build_dependencies install_project

build_dependencies:
	echo -e "${LGRN_COLOR}build_dependencies:${NORM_COLOR}"
	python -m pip install --upgrade pip
	pip install -r requirements.txt
install_project:
	echo -e "${LGRN_COLOR}install project:${NORM_COLOR}"
	poetry install
	python manage.py collectstatic --no-input
	python manage.py migrate
lint:
	poetry run flake8 task_manager
dev:
	python3 manage.py runserver
messages:
	python manage.py makemessages -l ru
compile:
	python manage.py compilemessages
commit:
	git add -A
	git commit
amend:
	git add -A
	git commit --amend --no-edit
	git push --force
test:
	python manage.py test --noinput -v 2
test-coverage:
	coverage run --source='.' manage.py test
	coverage xml
start:
	poetry run python -m gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager:application