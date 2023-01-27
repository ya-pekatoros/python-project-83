import pytest
from page_analyzer import app


@pytest.fixture()
def test_app():
    app.config['SECRET_KEY'] = 'SUPER-SECRET-KEY'
    app.config['DATABASE_URL'] = 'TEST_URL'
    app.testing = True
    return app


@pytest.fixture()
def client(test_app):
    return test_app.test_client()
