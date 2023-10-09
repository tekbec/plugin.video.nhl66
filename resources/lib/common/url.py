import base64

def encode_proxy_url(url: str):
    ext = url.split('.')[-1]
    if len(ext) > 5:
        ext = None
    encoded_url = 'http://localhost:20568/' + base64.b64encode(url.encode('utf-8')).decode('utf-8')
    if ext:
        encoded_url += '.' + ext
    return encoded_url

def decode_proxy_url(url: str):
    url = url.split('.')[0]
    decoded_url = base64.b64decode(url.encode('utf-8')).decode('utf-8')
    return decoded_url
    
def urljoin(base: str, path: str):
    if not base.endswith('/'):
        base += '/'
    if path.startswith('/'):
        path = path[1:]
    return base + path
    