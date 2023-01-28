import requests


def make_external_req(url):
    message = None
    status_code = None
    try:
        status_code = requests.get(url).status_code
    except Exception:
        message = 'Произошла ошибка при проверке'
    return {'status_code': status_code, 'message': message}
