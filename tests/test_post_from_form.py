from unittest import mock
import datetime

DATABASE_URL = 'TEST_URL'


def test_post_from_form(client, test_app):
    with mock.patch('psycopg2.connect', autospec=True) as mock_connect:
        mock_con_cm = mock_connect.return_value  # result of psycopg2.connect(**connection_stuff)
        mock_con = mock_con_cm.__enter__.return_value  # object assigned to con in with ... as con
        mock_cur_cm = mock_con.cursor.return_value  # result of con.cursor(cursor_factory=DictCursor)
        mock_cur = mock_cur_cm.__enter__.return_value  # object assigned to cur in with ... as cur
        response = client.post('/', data={
            'url': "https://google.com",
        }, follow_redirects=True)
        assert response.status_code == 200
        mock_connect.assert_called_with(test_app.config['DATABASE_URL'])
        today = datetime.date.today().isoformat()
        mock_cur.execute.assert_called_with('INSERT INTO urls (name, created_at) VALUES (%s, %s)',
                                            ('https://google.com', today))
        flash_mes = 'Страница успешно добавлена'.encode("utf-8", "ignore")
        assert flash_mes in response.data
        mock_cur.fetchone.return_value = ("https://google.com",)
        response = client.post('/', data={
            'url': "https://google.com",
        }, follow_redirects=True)
        mock_cur.execute.assert_called_with('SELECT name FROM urls WHERE name = %s',
                                            ('https://google.com',))
        flash_mes = 'Страница уже существует'.encode("utf-8", "ignore")
        assert flash_mes in response.data
