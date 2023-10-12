from .url import encode_proxy_url
import requests

SESSIONS = {}

def get(url: str, provider: str = None, headers: dict = None, skip_cache: bool = False):
    encoded_url = encode_proxy_url(url, headers, provider, skip_cache)
    return requests.get(encoded_url)