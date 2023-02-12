from datetime import datetime
from unittest import mock

DATABASE_URL = 'TEST_URL'


def test_url(client, test_app):
    with mock.patch('psycopg2.connect', autospec=True) as mock_connect:
        mock_con_cm = mock_connect.return_value  # result of psycopg2.connect(**connection_stuff)
        mock_con = mock_con_cm.__enter__.return_value  # object assigned to con in with ... as con
        mock_cur_cm = mock_con.cursor.return_value  # result of con.cursor(cursor_factory=DictCursor)
        mock_cur = mock_cur_cm.__enter__.return_value  # object assigned to cur in with ... as cur
        mock_cur.fetchone.return_value = (
            '1', 'https://ru.hexlet.io', datetime.strptime("26-01-2023", "%d-%m-%Y")
        )
        mock_cur.fetchall.return_value = [
            ('1', '1', 'None', 'None', 'None', 'None', datetime.strptime("26-01-2023", "%d-%m-%Y")),
            ('2', '1', 'None', 'None', 'None', 'None', datetime.strptime("26-01-2023", "%d-%m-%Y"))
        ]
        response = client.get('/urls/1', follow_redirects=True)
        assert response.status_code == 200
        mock_connect.assert_called_with(test_app.config['DATABASE_URL'])
        mock_cur.execute.assert_any_call("SELECT id, name, created_at "
                                         "FROM urls WHERE id = %s", ('1',))
        mock_cur.execute.assert_any_call("SELECT id, url_id, status_code, h1, title, description, "
                                         "created_at FROM url_checks "
                                         "WHERE url_id = %s ORDER BY id DESC", ('1',))
        (id, name, date) = mock_cur.fetchone.return_value
        [(id1, id, _, _, _, _, created_at1),
         (id2, _, _, _, _, _, created_at2)] = mock_cur.fetchall.return_value
        (id, name, date) = mock_cur.fetchone.return_value
        assert id.encode("utf-8", "ignore") in response.data
        assert name.encode("utf-8", "ignore") in response.data
        assert date.strftime('%d-%m-%Y').encode("utf-8", "ignore") in response.data
        assert id1.encode("utf-8", "ignore") in response.data
        assert id2.encode("utf-8", "ignore") in response.data
        assert created_at1.strftime('%d-%m-%Y').encode("utf-8", "ignore") in response.data
        assert created_at2.strftime('%d-%m-%Y').encode("utf-8", "ignore") in response.data
