install:
		poetry install

# возможно не нужна команда
build:
		poetry build

# возможно не нужна команда
publish:
		poetry publish --dry-run

# возможно не нужна команда
package-install:
		python3 -m pip install --force-reinstall --user dist/*.whl

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

.PHONY: install