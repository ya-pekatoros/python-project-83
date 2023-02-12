import validators


def validator(url):
    if len(url) > 255:
        return {'result': False, 'message': 'URL превышает 255 символов'}
    if not validators.url(url):
        return {'result': False, 'message': 'Некорректный URL'}
    return {'result': True}
