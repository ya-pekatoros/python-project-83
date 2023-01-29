import requests


def make_external_req(url):
    message = None
    status_code = None
    data = None
    try:
        request_result = requests.get(url)
        status_code = request_result.status_code
        if status_code == 200:
            data = request_result.text
        else:
            raise Exception
    except Exception:
        message = 'Произошла ошибка при проверке'
    return {'status_code': status_code, 'message': message, 'data': data}
