install:
		poetry install

# возможно не нужна команда
build:
		poetry build

build-db: db-drop db-create schema-data-load

db-start:
		sudo service postgresql start >./database/logfile 2>&1 &

db-status:
		sudo service postgresql status

db-stop:
		sudo service postgresql stop

db-create:
		createdb third-project

db-drop:
		dropdb third-project

db-reset:
	dropdb third-project || true
	createdb third-project

dbs-show:
		psql -l

db-connect:
	psql -d third-project

dev-setup: db-reset schema-data-load

schema-data-load:
		psql third-project < database.sql

db-show-log:
		vim /var/log/postgresql/postgresql-14-main.log

dev:
		poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
		poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
		{ \
    	poetry run flake8 page_analyzer;\
		poetry run flake8 tests;\
    	}

test:
		poetry run pytest

tests-cov:
		poetry run pytest --cov=page_analyzer --cov-report xml

show-active-ports:
		sudo lsof -i -P -n | grep LISTEN
# kill -9 processid - force comand to kill process

.PHONY: install