import requests

base_url = "http://127.0.0.1:5000/"


def get():
    print(requests.get(base_url).text)
