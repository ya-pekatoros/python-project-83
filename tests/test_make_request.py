from page_analyzer import make_request
from unittest import mock
import requests


def test_make_request():
    with mock.patch('requests.get') as mock_external_req:
        mock_external_req('https://google.com').status_code = 200
        mock_external_req('https://google.com').text = 'Data'
        assert make_request('https://google.com') == {
            'status_code': 200,
            'result': True,
            'data': 'Data'
        }
        mock_external_req.side_effect = requests.exceptions.HTTPError
        assert make_request('https://.com') == {
            'status_code': None,
            'result': False,
            'data': None
        }
