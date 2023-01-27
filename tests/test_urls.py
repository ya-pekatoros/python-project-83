from unittest import mock

DATABASE_URL = 'TEST_URL'


def test_urls(client, test_app):
    with mock.patch('psycopg2.connect', autospec=True) as mock_connect:
        mock_con_cm = mock_connect.return_value  # result of psycopg2.connect(**connection_stuff)
        mock_con = mock_con_cm.__enter__.return_value  # object assigned to con in with ... as con
        mock_cur_cm = mock_con.cursor.return_value  # result of con.cursor(cursor_factory=DictCursor)
        mock_cur = mock_cur_cm.__enter__.return_value  # object assigned to cur in with ... as cur
        mock_cur.fetchall.return_value = ([('1', 'https://ru.hexlet.io', '26-01-2023'),
                                           ('2', 'https://google.com', '26-01-2023'),
                                           ('3', 'https://blizzard.com', '26-01-2023')])
        response = client.get('/urls', follow_redirects=True)
        assert response.status_code == 200
        mock_connect.assert_called_with(test_app.config['DATABASE_URL'])
        mock_cur.execute.assert_called_with("SELECT id, name, TO_CHAR(created_at, 'DD-MM-YYYY') "
                                            "FROM urls ORDER BY id DESC LIMIT 30")
        [(id1, name1, date1), (id2, name2, date2), (id3, name3, date3)] = mock_cur.fetchall.return_value
        assert id1.encode("utf-8", "ignore") in response.data
        assert name1.encode("utf-8", "ignore") in response.data
        assert date1.encode("utf-8", "ignore") in response.data
        assert id2.encode("utf-8", "ignore") in response.data
        assert name2.encode("utf-8", "ignore") in response.data
        assert date2.encode("utf-8", "ignore") in response.data
        assert id3.encode("utf-8", "ignore") in response.data
        assert name3.encode("utf-8", "ignore") in response.data
        assert date3.encode("utf-8", "ignore") in response.data
