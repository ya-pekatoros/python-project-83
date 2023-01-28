from page_analyzer import make_external_req
from unittest import mock


def test_make_external_req():
    with mock.patch('requests.get') as mock_external_req:
        mock_external_req('https://google.com').status_code = 200
        assert make_external_req('https://google.com') == {'status_code': 200, 'message': None}
        mock_external_req.side_effect = Exception('URLError')
        assert make_external_req('https://.com') == {'status_code': None, 'message': 'Произошла ошибка при проверке'}
