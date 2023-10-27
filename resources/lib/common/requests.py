from .url import encode_proxy_url
import requests

def get(url: str, provider: str = None, headers: dict = None, skip_cache: bool = False):
    encoded_url = encode_proxy_url(url, headers, provider, skip_cache)
    return requests.get(encoded_url)

def post(url: str, json = dict, provider: str = None, headers: dict = None, skip_cache: bool = False):
    if headers is None:
        headers = {}
    headers['Content-Type'] = 'application/json'
    encoded_url = encode_proxy_url(url, headers, provider, skip_cache)
    return requests.post(encoded_url, json=json)
