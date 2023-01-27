from unittest import mock
import datetime

DATABASE_URL = 'TEST_URL'


def test_add_url(client, test_app):
    with mock.patch('psycopg2.connect', autospec=True) as mock_connect:
        mock_con_cm = mock_connect.return_value  # result of psycopg2.connect(**connection_stuff)
        mock_con = mock_con_cm.__enter__.return_value  # object assigned to con in with ... as con
        mock_cur_cm = mock_con.cursor.return_value  # result of con.cursor(cursor_factory=DictCursor)
        mock_cur = mock_cur_cm.__enter__.return_value  # object assigned to cur in with ... as cur
        today = datetime.date.today().isoformat()
        mock_cur.fetchone.return_value = ('1', "_", today)
        response = client.post('/', data={
            'url': "https://google.com",
        }, follow_redirects=True)
        assert response.status_code == 200
        mock_connect.assert_called_with(test_app.config['DATABASE_URL'])
        mock_cur.execute.assert_any_call("SELECT id, name FROM urls WHERE name = %s",
                                         ('https://google.com',))
        mock_cur.execute.assert_any_call('INSERT INTO urls (name, created_at) VALUES (%s, %s)',
                                         ('https://google.com', today))
        mock_cur.execute.assert_any_call("SELECT id FROM urls WHERE name = %s",
                                         ('https://google.com',))
        flash_mes = 'Страница успешно добавлена'.encode("utf-8", "ignore")
        assert flash_mes in response.data
        assert today.encode("utf-8", "ignore") in response.data

        mock_cur.fetchone.return_value = ('1', "https://asus.com", '26-01-2023')
        response = client.post('/', data={
            'url': "https://asus.com",
        }, follow_redirects=True)
        mock_cur.execute.assert_any_call("SELECT id, name FROM urls WHERE name = %s",
                                         ("https://asus.com",))
        flash_mes = 'Страница уже существует'.encode("utf-8", "ignore")
        data1 = "https://asus.com".encode("utf-8", "ignore")
        assert data1 in response.data
        assert flash_mes in response.data

        response = client.post('/', data={
            'url': "google.com",
        }, follow_redirects=True)
        flash_mes = 'Некорректный URL'.encode("utf-8", "ignore")
        assert flash_mes in response.data
