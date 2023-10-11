from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .common.url import encode_proxy_url, decode_proxy_url, urljoin
from .common.requests import get, head
from codequick.script import Script
import requests, re, urllib.parse

PASSTHROUGH_HEADERS = [
    'Age',
    'Cache-Control',
    'Content-Encoding',
    'Content-Length',
    'Content-Type',
    'Date',
    'Etag',
    'Expires',
    'Last-Modified',
    'Vary',
    'Via',
]
CACHE = {}
CACHE_SIZE = 20
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
NHL66_ESPN_CYPER_BASE_URL = 'https://api.nhl66.ir/api/get_cypher/espn'

class RequestsHandler(BaseHTTPRequestHandler):

    def do_GET(self, method='GET', send_body=True):
        # Decode the url
        decoded_url = decode_proxy_url(self.path.lstrip('/'))

        # Print the request
        provider = None
        if 'espn' in decoded_url:
            Script.log(f'[ESPN] [{method}] {decoded_url}', lvl=Script.DEBUG)
            provider = 'espn'
        else:
            Script.log(f'[?] [{method}] {decoded_url}', lvl=Script.DEBUG)

        # Try to find the response in the cache
        if decoded_url in CACHE:
            Script.log(f'Cache hit.', lvl=Script.DEBUG)
            resp = CACHE[decoded_url]
        # Try to make the request
        else:
            # Make the request
            try:
                resp = get(decoded_url, provider)
            # On request error (most-likely proxy error), send a 500 response
            except Exception as e:
                Script.log(f'Request error. Responding with a 500 (INTERNAL SERVER ERROR).', lvl=Script.ERROR)
                Script.log(str(e), lvl=Script.DEBUG)
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                if send_body:
                    self.wfile.write(b'Internal Server Error')
                Script.log(f'Response code: 500.', lvl=Script.DEBUG)
                return
            # Limit the cache size
            if len(CACHE) >= CACHE_SIZE:
                CACHE.pop(next(iter(CACHE)))
            # Cache the response if it's a media format
            if decoded_url.endswith('.ts'):
                CACHE[decoded_url] = resp
            Script.log(f'Cache size: {str(len(CACHE))}.', lvl=Script.DEBUG)

        # These are for response that can be returned as-is
        if resp.status_code < 200 or resp.status_code > 299 or decoded_url.endswith('.ts') or 'nhl66' in decoded_url:
            self.send_response(resp.status_code)
            for key, val in resp.headers.items():
                if PASSTHROUGH_HEADERS is None or key.lower() in PASSTHROUGH_HEADERS:
                    self.send_header(key, val)
            self.end_headers()
            if send_body:
                self.wfile.write(resp.content)
            Script.log(f'Response code: {resp.status_code}.', lvl=Script.DEBUG)
            return

        # Modify the body ()
        body = resp.text
        base_url = decoded_url.rsplit('/', 1)[0]
        lines = body.split('\n')
        for i in range(len(lines)):
            try:
                # This is meant to redirect manifest and segment requests
                if lines[i].endswith('.m3u8') or lines[i].endswith('.ts'):
                    url = lines[i]
                    if not lines[i].startswith('http'):
                        url = urljoin(base_url, url)
                    lines[i] = encode_proxy_url(url)
                # This is meant to redirect license requests
                elif lines[i].strip().upper().startswith('#EXT-X-KEY:METHOD'):
                    old_url = re.findall(r'"(http.*)"', lines[i])[0]
                    new_url = NHL66_ESPN_CYPER_BASE_URL + urllib.parse.urlparse(old_url).path
                    encoded_url = encode_proxy_url(new_url)
                    lines[i] = lines[i].replace(old_url, encoded_url)
            except Exception as e:
                Script.log(str(e), lvl=Script.ERROR)
        body = '\n'.join(lines)

        self.send_response(resp.status_code)
        for key, val in resp.headers.items():
            if PASSTHROUGH_HEADERS is None or key.lower() in PASSTHROUGH_HEADERS:
                self.send_header(key, val)
        self.end_headers()
        if send_body:
            self.wfile.write(body.encode())
        Script.log(f'Response code: {resp.status_code}.', lvl=Script.DEBUG)
    
    def do_HEAD(self):
        self.do_GET(method='HEAD', send_body=False)

        


def run():
    server_address = ('', 20568)
    httpd = ThreadingHTTPServer(server_address, RequestsHandler)
    httpd.serve_forever()