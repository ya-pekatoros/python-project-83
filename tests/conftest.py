import pytest
from page_analyzer import app


@pytest.fixture
def test_app():
    return app


@pytest.fixture
def client(test_app):
    test_app.testing = True
    return app.test_client()
