from page_analyzer import get_url_data
from tests.fixtures.test_html_data import test_data


def test_get_url_data():
    for data, expectation in test_data:
        assert get_url_data(data) == expectation
