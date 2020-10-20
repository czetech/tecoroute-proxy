from asyncio import get_event_loop
from base64 import b64decode, b64encode
import binascii
from hashlib import sha1
from json import JSONDecodeError, dumps, loads
from typing import Awaitable, Callable, Optional
from urllib.parse import urljoin, urlparse
import zlib

from tornado import gen
from tornado.httpclient import HTTPClientError, HTTPRequest
from tornado.httpserver import HTTPServer
from tornado.httputil import (
    HTTPConnection, HTTPHeaders, HTTPServerRequest, ResponseStartLine
)

try:
    from tornado.curl_httpclient import CurlAsyncHTTPClient as AsyncHTTPClient
except ImportError:
    from tornado.simple_httpclient import (
        SimpleAsyncHTTPClient as AsyncHTTPClient
    )

AGENT_NAME = ('tecoroute-proxy/1.0 '
              '(+https://github.com/czetech/tecoroute-proxy)')


class Proxy:
    """"""

    def __init__(self, host: str='0.0.0.0', port: int=8080,
                 url: str='https://route.tecomat.com') -> None:
        self._host = host
        self._port = port
        self._url = url
        self._http = HTTPServer(self._process_request)
    
    @property
    def client_name(self) -> str:
        """Returns the name of the Tornado HTTP client used.
        
        If available, "CurlAsyncHTTPClient" is used, otherwise
        "SimpleAsyncHTTPClient" is used. The availability of
        CurlAsyncHTTPClient can be debugged using
        `import tornado.curl_httpclient.CurlAsyncHTTPClient` in Python
        environment (PycURL must be present).
        """
        return AsyncHTTPClient.__name__
    
    @gen.coroutine
    def _process_request(self, request: HTTPServerRequest) -> None:
        connection = request.connection
        try:
            cookie_data = request.cookies['tecoroute-proxy'].value
            data = loads(zlib.decompress(b64decode(cookie_data)).decode())
        except (JSONDecodeError, zlib.error, binascii.Error, KeyError):
            data = {}
        response_headers = HTTPHeaders({'Server': AGENT_NAME})
        
        if (urlparse(request.uri).path == '/tecoroute-proxy'
            and (request.method == 'GET' or request.method == 'POST')):
            print(request.arguments)
            raise
        
        tr_cookie = request.cookies
        
        tr_client = AsyncHTTPClient()
        tr_url = urljoin(self._url, request.uri)
        tr_cookiestr = '; '.join(key + '=' + morsel.coded_value for key, morsel
                              in tr_cookie.items())
        tr_body = None if request.method == 'GET' else request.body
        tr_request = HTTPRequest(tr_url, request.method,
                                 {'Cookie': tr_cookiestr},
                                 tr_body, follow_redirects=False,
                                 user_agent=AGENT_NAME,
                                 allow_nonstandard_methods=True)
        try:
            tr_response = yield tr_client.fetch(tr_request, raise_error=False)
        except HTTPClientError:
            response_start_line = ResponseStartLine(None, 502,
                                                    'Bad Tecoroute Gateway')
            connection.write_headers(response_start_line, response_headers)
            connection.finish()
        
        response_start_line = ResponseStartLine(None, tr_response.code,
                                                tr_response.reason)
        response_headers_keys = response_headers.keys()
        for name, value in tr_response.headers.get_all():
            if name not in response_headers_keys:
                response_headers.add(name, value)
        connection.write_headers(response_start_line, tr_response.headers)
        connection.write(tr_response.body)
        connection.finish()
    
    def start(self) -> None:
        """Starts Tecoroute proxy server in current event loop."""
        self._http.listen(self._port, self._host)


if __name__ == '__main__':
    proxy = Proxy()
    print(proxy.client_name)
    proxy.start()
    get_event_loop().run_forever()
