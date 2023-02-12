import requests


def make_request(url):
    status_code = None
    data = None
    try:
        request_result = requests.get(url)
        request_result.raise_for_status()
        status_code = request_result.status_code
        data = request_result.text
        result = True
    except requests.exceptions.RequestException:
        result = False
    return {'status_code': status_code, 'result': result, 'data': data}
