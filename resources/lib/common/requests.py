from codequick.script import Settings, Script
from copy import copy
import requests

def get_proxies(provider: str):
    if provider == None:
        return None
    val = Settings.get_string(f'{provider}_proxy')
    if not val:
        return None
    return {
        'http': str(val),
        'https': str(val)
    }

def get_headers(headers: dict = None):
    return overlap_headers({
        'User-Agent': str(Settings.get_string('user_agent')),
    }, headers)

def overlap_headers(headers, priority_headers):
    if headers is None:
        return priority_headers
    elif priority_headers is None:
        return headers
    
    new_headers = copy(headers)
    for ik, iv in priority_headers.items():
        f = False
        for jk, jv in new_headers.items():
            if ik.lower() == jk.lower():
                new_headers[jk] = iv
                f = True
                break
        if not f:
            new_headers[ik] = iv
    
    return new_headers

def get(url: str, provider: str = None, headers: dict = None):
    new_headers = get_headers(headers)
    proxies = get_proxies(provider)

    Script.log(f'Making request to the following url: {url}', lvl=Script.DEBUG)
    Script.log(f'Making request with the following user agent: {new_headers.get("User-Agent", "")}', lvl=Script.DEBUG)
    if proxies:
        Script.log(f'Making request with the following proxy: {proxies.get("https", "")}', lvl=Script.DEBUG)
    else:
        Script.log('Making request with no proxy.', lvl=Script.DEBUG)
    return requests.get(url, headers=new_headers, proxies=proxies)
