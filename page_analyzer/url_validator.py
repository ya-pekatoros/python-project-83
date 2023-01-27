from urllib.parse import urlparse
import validators


def url_parser(url):
    if len(url) > 255:
        return {'result': False, 'message': 'URL превышает 255 символов'}
    if validators.url(url) is not True:
        return {'result': False, 'message': 'Некорректный URL'}
    url_parsed = urlparse(url)._replace(fragment="", params="", query="", path="").geturl()
    url_parsed = url_parsed.replace("www.", "")
    return {'result': True, 'message': url_parsed}
