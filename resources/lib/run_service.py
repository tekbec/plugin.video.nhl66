from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .common.url import encode_proxy_url, decode_proxy_url, urljoin
from .common.requests import get
from codequick.script import Script
import requests, re, urllib.parse

PASSTHROUGH_HEADERS = ['content-type']
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
NHL66_ESPN_CYPER_BASE_URL = 'https://api.nhl66.ir/api/get_cypher/espn'

class RequestsHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        decoded_url = decode_proxy_url(self.path.lstrip('/'))

        # Set the proxy
        provider = None
        if 'espn' in decoded_url:
            print('[NHL66] [ESPN] [GET] ' + decoded_url)
            provider = 'espn'
        else:
            print('[NHL66] [?] [GET] ' + decoded_url)

        # Make the request
        resp = get(decoded_url, provider)

        # These are for response that can be returned as-is
        if resp.status_code < 200 or resp.status_code > 299 or decoded_url.endswith('.ts') or 'nhl66' in decoded_url:
            self.send_response(resp.status_code)
            for key, val in resp.headers.items():
                if key.lower() in PASSTHROUGH_HEADERS:
                    self.send_header(key, val)
            self.end_headers()
            self.wfile.write(resp.content)
            return

        body = resp.text
        # Modify the body
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
                if key.lower() in PASSTHROUGH_HEADERS:
                    self.send_header(key, val)
        self.end_headers()
        self.wfile.write(body.encode())


def run():
    server_address = ('', 20568)
    httpd = ThreadingHTTPServer(server_address, RequestsHandler)
    httpd.serve_forever()