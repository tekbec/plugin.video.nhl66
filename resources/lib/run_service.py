from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .common.url import encode_proxy_url, decode_proxy_url, urljoin
from codequick.script import Script, Settings
from copy import copy
from datetime import datetime, timedelta
from requests.structures import CaseInsensitiveDict
from requests.exceptions import ProxyError
from .exceptions import NotificationError
import requests, re, urllib.parse, traceback, json, xbmcaddon, xbmcgui

# For how many seconds cached responses should be valid
CACHE_VALIDITY_DURATION = {
    'nhltv': -1,
    'espn': -1,
    'nhl66': 60
}

# Headers that should be kept intact
PASSTHROUGH_HEADERS = [x.lower() for x in [
    'Content-Type',
]]

# Headers that will be added to the response depending on provider
CUSTOM_RESPONSE_HEADERS = {
    '*': {},
    'nhl66': {},
    'espn': {},
    'nhltv': {},
}

PROVIDER_NAMES = {
    'espn': 'ESPN',
    'nhltv': 'NHL.TV',
    'nhl66': 'NHL66'
}

ADDON_DATA = xbmcaddon.Addon()
ADDON_ICON = ADDON_DATA.getAddonInfo('icon')

CACHE = {}
CACHE_SIZE = 20
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
NHL66_ESPN_CYPER_BASE_URL = 'https://api.nhl66.ir/api/get_cypher/espn'

class RequestsHandler(BaseHTTPRequestHandler):

    SESSIONS = {}

    def log(self, msg, lvl=Script.DEBUG):
        '''
        Creates an entry in Kodi's log
        '''

        Script.log(f'[PROXY] {msg}', lvl=lvl)

    # -------------------------------------------------------- #
    #
    # HANDLERS
    #
    # -------------------------------------------------------- #

    def do_GET(self, method='GET'):
        '''
        Handles incoming GET requests
        '''

        try:
            # -------------------------------------------------------- #
            # Get informations about the request to make
            # -------------------------------------------------------- #
            request_info = decode_proxy_url(self.path)
            self.skip_cache = request_info['skip_cache']
            self.headers = CaseInsensitiveDict(request_info['headers'])
            self.url = request_info['url']
            self.extension = request_info['ext']
            self.filename = urllib.parse.urlparse(self.url).path.split('/')[-1]
            self.method = method
            self.provider = request_info['provider']


            # -------------------------------------------------------- #
            # Make the request
            # -------------------------------------------------------- #
            try:
                resp = self._get_response()
            except ProxyError:
                self.log('Proxy Error.', Script.ERROR)
                traceback.print_exc()
                dialog = xbmcgui.Dialog()
                dialog.notification('Proxy Error', f'Unable to connect to {PROVIDER_NAMES.get(self.provider, "unknown")} proxy.', ADDON_ICON)
                return self._send(500, {'Content-Type': 'text/plain'}, b'Proxy Error')
            except:
                self.log('Unable to make request.', Script.ERROR)
                traceback.print_exc()
                return self._send(500, {'Content-Type': 'text/plain'}, b'Internal Server Error')


            # -------------------------------------------------------- #
            # Requests that need no changes
            # -------------------------------------------------------- #
            if self.provider == 'nhl66' or \
                resp.status_code < 200 or resp.status_code > 299 or \
                self.extension == 'ts':
                return self._send(resp.status_code, self._filter_headers(resp.headers), resp.content)
            body = resp.text


            # -------------------------------------------------------- #
            # M3U8 requests
            # -------------------------------------------------------- #
            if self.extension == 'm3u8':
                self.log('.m3u8 file detected, modifiying hrefs...')
                base_url = self.url.rsplit('/', 1)[0]
                lines = body.split('\n')
                for i in range(len(lines)):
                    try:

                        # Remove the query string (this allows us to get the extension of the url)
                        url_without_qs = lines[i]
                        try:
                            url_without_qs = lines[i][:lines[i].index('?')]
                        except:
                            pass

                        # Redirect manifests and segments requests
                        if url_without_qs.endswith('.m3u8') or url_without_qs.endswith('.ts'):
                            segment_url = lines[i]
                            if not lines[i].startswith('http'):
                                segment_url = urljoin(base_url, segment_url)
                            lines[i] = encode_proxy_url(segment_url, provider=self.provider)

                        # Redirect license requests
                        elif lines[i].strip().upper().startswith('#EXT-X-KEY:METHOD'):
                            old_url = re.findall(r'"(http.*)"', lines[i])[0]
                            new_url = ''
                            # ESPN license requests must be redirected to NHL66
                            if self.provider == 'espn':
                                new_url = NHL66_ESPN_CYPER_BASE_URL + urllib.parse.urlparse(old_url).path
                                new_url = encode_proxy_url(new_url, provider='nhl66')
                            # NHL.TV license requests don't need any additionnal redirect
                            elif self.provider == 'nhltv':
                                new_url = encode_proxy_url(old_url, provider='nhl66')
                            lines[i] = lines[i].replace(old_url, new_url)
                    except:
                        self.log(f'Unable to parse this line: {lines[i]}', Script.ERROR)
                        traceback.print_exc()
                body = '\n'.join(lines)

            self._send(resp.status_code, self._filter_headers(resp.headers), body.encode())
        except:
            self.log('Unhandled exception.', Script.ERROR)
            traceback.print_exc()
            self._send(500, {'Content-Type': 'text/plain'}, b'Internal Server Error')
    


    def do_HEAD(self):
        '''
        Handles incoming HEAD requests
        '''
        self.do_GET(method='HEAD')



    # -------------------------------------------------------- #
    #
    # REQUESTS
    #
    # -------------------------------------------------------- #



    def _get_response(self):
        '''
        Returns the response for the requested data.
        This will return the cached response if available and valid.
        '''
        response = None
        if not self.skip_cache:
            response = self._search_cache()
        else:
            self.log('Cache skipped.')
        if response is not None:
            return response
        response = self._make_request()
        self._save_cache(response)
        return response
    


    def _make_request(self):
        '''
        Makes the GET request and returns the response.
        '''

        session = self._get_provider_session(self.provider)
        new_headers = self._add_provider_headers(self.headers)
        proxies = self._get_provider_proxies(self.provider)

        self.log(f'URL.......: {self.url}')
        self.log(f'User Agent: {new_headers.get("User-Agent", None)}')
        if proxies:
            self.log(f'Proxy.....: {proxies.get("https", "")}')
        else:
            self.log('Proxy.....: None')
        return session.get(self.url, headers=new_headers, proxies=proxies)
    


    def _get_provider_session(self, provider: str = None) -> requests.Session:
        '''
        Returns the provider session.
        '''
        if not (str(provider)) in RequestsHandler.SESSIONS:
            RequestsHandler.SESSIONS[str(provider)] = requests.Session()
        return RequestsHandler.SESSIONS[str(provider)]
    


    def _add_provider_headers(self, headers: CaseInsensitiveDict = None):
        '''
        Returns headers with mandatory provider headers added to it.
        '''
        new_headers = CaseInsensitiveDict({})
        if headers is not None:
            for key, val in headers.items():
                new_headers[key] = val
        new_headers['User-Agent'] = str(Settings.get_string('user_agent'))
        return new_headers
    


    def _get_provider_proxies(self, provider: str):
        '''
        Returns the proxy assigned to the provider.
        '''
        if provider == None:
            return None
        val = Settings.get_string(f'{provider}_proxy')
        if not val:
            return None
        return {
            'http': str(val),
            'https': str(val)
        }



    # -------------------------------------------------------- #
    #
    # CACHE
    #
    # -------------------------------------------------------- #



    def _search_cache(self):
        # Check if there is an entry in the cache
        if not self.url in CACHE.get(self.provider, {}):
            self.log('Cache miss.')
            return None
        # Check expiry
        entry = CACHE.get(self.provider, {})[self.url]
        if entry['expiry']:
            if datetime.timestamp(datetime.now()) > entry['expiry']:
                self.log('Cache entry expired.')
                return None
        # No expiry: cache hit
        self.log('Cache hit.')
        return entry['response']
    


    def _save_cache(self, response):
        
        # Filter
        if (self.provider == 'nhltv' and (self.filename == 'master-archive.m3u8' or self.filename == 'master.m3u8')) or \
            (self.provider == 'nhl66'):

            # Expiry
            expiry = None
            validy_duration = CACHE_VALIDITY_DURATION.get(self.provider, -1)
            if validy_duration > 0:
                expiry = datetime.timestamp(datetime.now() + timedelta(0,validy_duration))
            # Save in cache
            if not self.provider in CACHE:
                CACHE[self.provider] = {}
            CACHE[self.provider][self.url] = {
                'response': response,
                'expiry': expiry
            }
            
            # Limit cache size
            if len(CACHE[self.provider]) > CACHE_SIZE:
                CACHE[self.provider].pop(next(iter(CACHE[self.provider])))
            self.log(f'Saved to cache. New cache size: {str(len(CACHE[self.provider]))}')
        


    # -------------------------------------------------------- #
    #
    # RESPONSE
    #
    # -------------------------------------------------------- #



    def _send(self, code: int, headers: dict = None, body: bytes = None):
        '''
        Sends a response to the client.
        '''

        # Send response code
        self.send_response(code)

        # Calculate content length
        content_length = 0
        if body is not None:
            content_length = len(body)
        
        # Set headers
        merged_headers = CaseInsensitiveDict({})
        if headers is not None:
            for key, val in headers.items():
                merged_headers[key] = val
        if '*' in CUSTOM_RESPONSE_HEADERS:
            for key, val in CUSTOM_RESPONSE_HEADERS['*'].items():
                merged_headers[key] = val
        if self.provider in CUSTOM_RESPONSE_HEADERS:
            for key, val in CUSTOM_RESPONSE_HEADERS[self.provider].items():
                merged_headers[key] = val
        merged_headers['Content-Length'] = str(content_length)
        for key, val in merged_headers.items():
            self.send_header(key, val)
        self.end_headers()

        # Send body, except if method is HEAD
        if body is not None and self.method != 'HEAD':
            self.wfile.write(body)
        
        # Log the request
        self.log(f'<{str(self.method)}> <{str(self.provider)}> "../{str(self.filename)}" {str(code)} {str(content_length)}')

        # Log whole request (should be commented)
        if False:
            print('Headers:')
            for key, val in merged_headers.items():
                print(f'{key}: {val}')
            print('Body:')
            print(str(body))


    def _filter_headers(self, headers: CaseInsensitiveDict) -> CaseInsensitiveDict:
        '''
        Filters provided headers before sending them as response headers.
        Only headers from PASSTHROUGH_HEADERS will are kept.
        '''

        filtered_headers = CaseInsensitiveDict({})
        for key, val in headers.items():
            if PASSTHROUGH_HEADERS is None or key.lower() in PASSTHROUGH_HEADERS:
                filtered_headers[key] = val
        return filtered_headers



    

def run():
    server_address = ('', 20568)
    httpd = ThreadingHTTPServer(server_address, RequestsHandler)
    httpd.serve_forever()

