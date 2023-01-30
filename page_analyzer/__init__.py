from page_analyzer.external_request import make_request
from page_analyzer.get_data_from_url import get_url_data
from page_analyzer.app import app
from page_analyzer.url_validator import url_parser


__all__ = ['app', 'url_parser', 'make_request', 'get_url_data']
