from unittest import mock

DATABASE_URL = 'TEST_URL'


def test_url(client, test_app):
    with mock.patch('psycopg2.connect', autospec=True) as mock_connect:
        mock_con_cm = mock_connect.return_value  # result of psycopg2.connect(**connection_stuff)
        mock_con = mock_con_cm.__enter__.return_value  # object assigned to con in with ... as con
        mock_cur_cm = mock_con.cursor.return_value  # result of con.cursor(cursor_factory=DictCursor)
        mock_cur = mock_cur_cm.__enter__.return_value  # object assigned to cur in with ... as cur
        mock_cur.fetchone.return_value = ('1', 'https://ru.hexlet.io', '26-01-2023')
        response = client.get('/urls/1', follow_redirects=True)
        assert response.status_code == 200
        mock_connect.assert_called_with(test_app.config['DATABASE_URL'])
        mock_cur.execute.assert_called_with("SELECT id, name, TO_CHAR(created_at, 'DD-MM-YYYY') "
                                            "FROM urls WHERE id = %s", ('1',))
        (id, name, date) = mock_cur.fetchone.return_value
        assert id.encode("utf-8", "ignore") in response.data
        assert name.encode("utf-8", "ignore") in response.data
        assert date.encode("utf-8", "ignore") in response.data
