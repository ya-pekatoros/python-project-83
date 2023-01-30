import requests


def make_request(url):
    message = None
    status_code = None
    data = None
    try:
        request_result = requests.get(url)
        request_result.raise_for_status()
        status_code = request_result.status_code
        data = request_result.text
        message = 'Страница успешно проверена'
    except requests.exceptions.RequestException:
        message = 'Произошла ошибка при проверке'
    return {'status_code': status_code, 'message': message, 'data': data}
