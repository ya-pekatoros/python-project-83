from page_analyzer import parser


def test_parser():
    link_1 = 'https://google.com'
    link_2 = 'https://www.google.com/search?q=flask'
    assert parser(link_1) == 'https://google.com'
    assert parser(link_2) == 'https://google.com'
