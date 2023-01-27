from page_analyzer import url_parser


def test_url_parser():
    link_1 = (
        'https://google.com/111111111'
        '1111111111111111111111111111'
        '1111111111111111111111111111'
        '1111111111111111111111111111'
        '1111111111111111111111111111'
        '1111111111111111111111111111'
        '1111111111111111111111111111'
        '1111111111111111111111111111'
        '1111111111111111111111111111'
        '1111111111111111111111111111'
    )
    link_2 = 'google.con'
    link_2 = 'google.com'
    link_3 = 'https://google.com'
    link_4 = 'https://www.google.com/search?q=flask'
    assert url_parser(link_1) == {'result': False, 'message': 'URL превышает 255 символов'}
    assert url_parser(link_2) == {'result': False, 'message': 'Некорректный URL'}
    assert url_parser(link_3) == {'result': True, 'message': 'https://google.com'}
    assert url_parser(link_4) == {'result': True, 'message': 'https://google.com'}
