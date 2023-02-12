from page_analyzer import validator


def test_validator():
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
    assert validator(link_1) == {'result': False, 'message': 'URL превышает 255 символов'}
    assert validator(link_2) == {'result': False, 'message': 'Некорректный URL'}
    assert validator(link_3) == {'result': True}
    assert validator(link_4) == {'result': True}
