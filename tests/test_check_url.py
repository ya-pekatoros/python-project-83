from unittest import mock
import datetime
import requests

DATABASE_URL = 'TEST_URL'


def test_check_url(client, test_app):
    with mock.patch('psycopg2.connect', autospec=True) as mock_connect, \
         mock.patch('requests.get') as mock_external_req:
        mock_external_req('https://google.com').status_code = 200
        mock_external_req('https://google.com').text = '<html></html>'
        mock_con_cm = mock_connect.return_value  # result of psycopg2.connect(**connection_stuff)
        mock_con = mock_con_cm.__enter__.return_value  # object assigned to con in with ... as con
        mock_cur_cm = mock_con.cursor.return_value  # result of con.cursor(cursor_factory=DictCursor)
        mock_cur = mock_cur_cm.__enter__.return_value  # object assigned to cur in with ... as cur
        today = datetime.date.today()
        today_iso = today.isoformat()
        mock_cur.fetchone.return_value = ('1', "https://asus.com", datetime.datetime.strptime("27-01-2023", "%d-%m-%Y"))
        mock_cur.fetchall.return_value = [('1', "https://asus.com", 'None', 'None', 'None', 'None', today)]
        response = client.post('/urls/1/checks', data={'name': 'https://asus.com'}, follow_redirects=True)
        assert response.status_code == 200
        mock_connect.assert_called_with(test_app.config['DATABASE_URL'])
        mock_cur.execute.assert_any_call('INSERT INTO url_checks (url_id, status_code, created_at) '
                                         'VALUES (%s, %s, %s)', ('1', '200', today_iso))
        data1 = '<td>1</td>'.encode("utf-8", "ignore")
        data2 = today.strftime('%d-%m-%Y').encode("utf-8", "ignore")
        assert data1 in response.data
        assert data2 in response.data
        mock_external_req.side_effect = requests.exceptions.HTTPError
        response = client.post('/urls/1/checks', data={'name': 'https://asus.com'}, follow_redirects=True)
        flash_mess = 'Произошла ошибка при проверке'.encode("utf-8", "ignore")
        assert flash_mess in response.data
