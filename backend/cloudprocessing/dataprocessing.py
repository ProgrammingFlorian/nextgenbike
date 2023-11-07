import requests


def get_data_db():
    return requests.get('http://104.248.148.208/sensor').text
