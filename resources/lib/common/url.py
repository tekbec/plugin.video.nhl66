import base64, urllib.parse, json

def encode_proxy_url(url: str, headers: dict = None, provider: str = None, skip_cache = False):

    # Try to get the extension
    ext = urllib.parse.urlparse(url).path.split('.')[-1]
    if len(ext) > 5:
        ext = None
    
    # Ensure provider is a str
    if provider is None:
        provider = 'none'

    # Build the request info
    request_info = json.dumps({
        'url': url,
        'headers': headers,
        'provider': provider,
        'ext': ext,
        'skip_cache': skip_cache
    })

    # Build the URL
    encoded_url = f'http://localhost:20568/' + base64.b64encode(request_info.encode('utf-8')).decode('utf-8')
    if ext:
        encoded_url += '.' + ext
    return encoded_url

def decode_proxy_url(url: str):
    encoded_request_info = url.split('.')[0]
    if encoded_request_info.startswith('/'):
        encoded_request_info = encoded_request_info[1:]
    decoded_request_info = json.loads(base64.b64decode(encoded_request_info.encode('utf-8')).decode('utf-8'))
    return decoded_request_info
    
def urljoin(base: str, path: str):
    if not base.endswith('/'):
        base += '/'
    if path.startswith('/'):
        path = path[1:]
    return base + path
    