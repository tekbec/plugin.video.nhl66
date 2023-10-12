from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .common.url import encode_proxy_url, decode_proxy_url, urljoin
from codequick.script import Script, Settings
from copy import copy
from datetime import datetime, timedelta
import requests, re, urllib.parse


CACHE_VALIDITY_DURATION = {
    'nhltv': -1,
    'espn': -1,
    'nhl66': 60
}
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

    SESSIONS = {}

    def log(self, msg, lvl=Script.DEBUG):
        Script.log(f'[PROXY] {msg}', lvl=lvl)

    def do_GET(self, method='GET', send_body=True):
        try:
            # Decode the url
            request_info = decode_proxy_url(self.path)
            decoded_url = request_info['url']
            provider = request_info['provider']
            ext = request_info['ext']
            skip_cache = request_info['skip_cache']
            headers = request_info['headers']

            # Log the request
            self.log(f'[{method}] [{provider}] [{str(ext)}] {decoded_url}')

            # Make the request
            try:
                resp = self._make_request(decoded_url, provider, headers, skip_cache=skip_cache)
            except Exception as e:
                self.log('Request error. Responding with a 500 (INTERNAL SERVER ERROR).', Script.ERROR)
                self.log(str(e), Script.ERROR)
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                if send_body:
                    self.wfile.write(b'Internal Server Error')
                self.log('Response code: 500.', Script.ERROR)
                return

            # These are for response that can be returned as-is
            if resp.status_code < 200 or resp.status_code > 299 or ext == 'ts' or provider == 'nhl66':
                self.send_response(resp.status_code)
                for key, val in resp.headers.items():
                    if PASSTHROUGH_HEADERS is None or key.lower() in PASSTHROUGH_HEADERS:
                        self.send_header(key, val)
                self.end_headers()
                if send_body:
                    self.wfile.write(resp.content)
                self.log(f'Response code: {resp.status_code}.')
                return

            
            body = resp.text

            # Modify m3u8 body
            if ext == 'm3u8':
                self.log('Modifying M3U8 response...')
                base_url = decoded_url.rsplit('/', 1)[0]
                lines = body.split('\n')
                for i in range(len(lines)):
                    try:
                        # Try to remove query string, if any
                        url_without_qs = lines[i]
                        try:
                            url_without_qs = lines[i][:lines[i].index('?')]
                        except:
                            pass
                        # This is meant to redirect manifest and segment requests
                        if url_without_qs.endswith('.m3u8') or url_without_qs.endswith('.ts'):
                            url = lines[i]
                            if not lines[i].startswith('http'):
                                url = urljoin(base_url, url)
                            lines[i] = encode_proxy_url(url, provider=provider)
                        # This is meant to redirect license requests
                        elif lines[i].strip().upper().startswith('#EXT-X-KEY:METHOD'):
                            old_url = re.findall(r'"(http.*)"', lines[i])[0]
                            encoded_url = ''
                            if provider == 'espn':
                                new_url = NHL66_ESPN_CYPER_BASE_URL + urllib.parse.urlparse(old_url).path
                                encoded_url = encode_proxy_url(new_url, provider='nhl66')
                            elif provider == 'nhltv':
                                encoded_url = encode_proxy_url(old_url, provider='nhl66')
                            lines[i] = lines[i].replace(old_url, encoded_url)
                    except Exception as e:
                        self.log(str(e), Script.ERROR)
                body = '\n'.join(lines)

            self.send_response(resp.status_code)
            for key, val in resp.headers.items():
                if PASSTHROUGH_HEADERS is None or key.lower() in PASSTHROUGH_HEADERS:
                    self.send_header(key, val)
            self.end_headers()
            if send_body:
                self.wfile.write(body.encode())
            self.log(f'Response code: {resp.status_code}.', lvl=Script.DEBUG)
        except Exception as e:
            self.log('Unexpected error. Responding with a 500 (INTERNAL SERVER ERROR).', Script.ERROR)
            self.log(str(e), Script.ERROR)
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            if send_body:
                self.wfile.write(b'Internal Server Error')
            self.log('Response code: 500.', Script.ERROR)
    
    def do_HEAD(self):
        self.do_GET(method='HEAD', send_body=False)

    def _get(self, url: str, provider: str = None, headers: dict = None):
        session = self.get_session(provider)
        new_headers = get_headers(headers)
        proxies = get_proxies(provider)

        self.log(f'Making request to the following url: {url}')
        self.log(f'Making request with the following user agent: {new_headers.get("User-Agent", "")}')
        if proxies:
            self.log(f'Making request with the following proxy: {proxies.get("https", "")}')
        else:
            self.log('Making request with no proxy.')
        return session.get(url, headers=new_headers, proxies=proxies)
    
    def get_session(self, provider: str = None) -> requests.Session:
        if not (str(provider)) in RequestsHandler.SESSIONS:
            RequestsHandler.SESSIONS[str(provider)] = requests.Session()
        return RequestsHandler.SESSIONS[str(provider)]
    
    def _make_request(self, url: str, provider: str, headers: dict = None, ext: str = None, skip_cache: bool = False):
        response = None
        if not skip_cache:
            response = self._search_cache(url, provider)
        else:
            self.log('Skipping cache.')
        if response is not None:
            return response
        response = self._get(url, provider, headers)
        self._save_cache(url, provider, response, ext)
        return response

    def _search_cache(self, url: str, provider: str):
        # Check if there is an entry in the cache
        if not url in CACHE.get(provider, {}):
            self.log('Cache miss.')
            return None
        # Check expiry
        entry = CACHE.get(provider, {})[url]
        if entry['expiry']:
            if datetime.timestamp(datetime.now()) > entry['expiry']:
                self.log('Cache entry expired.')
                return None
        # No expiry: cache hit
        self.log('Cache hit.')
        return entry['response']
    
    def _save_cache(self, url: str, provider: str, response, ext: str = None):
        # Filter
        if not (provider == 'nhl66' or ext == 'ts'):
            return
        # Expiry
        expiry = None
        validy_duration = CACHE_VALIDITY_DURATION.get(provider, -1)
        if validy_duration > 0:
            expiry = datetime.timestamp(datetime.now() + timedelta(0,validy_duration))
        # Save in cache
        if not provider in CACHE:
            CACHE[provider] = {}
        CACHE[provider][url] = {
            'response': response,
            'expiry': expiry
        }
        self.log('Saved to cache.')
        # Limit cache size
        if len(CACHE[provider]) > CACHE_SIZE:
            CACHE[provider].pop(next(iter(CACHE[provider])))
        self.log(f'Cache size: {str(len(CACHE[provider]))}')
        
        
        




        


def run():
    server_address = ('', 20568)
    httpd = ThreadingHTTPServer(server_address, RequestsHandler)
    httpd.serve_forever()

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