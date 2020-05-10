from loguru import logger
from http_parser.parser import HttpParser


EXAMPLE_RESPONSE = b"""HTTP/1.1 200 OK
Date: Sun, 10 Oct 2010 23:26:07 GMT
Server: namiko/1.0.0
Last-Modified: Sun, 26 Sep 2010 22:04:35 GMT
ETag: "45b6-834-49130cc1182c0"
Accept-Ranges: bytes
Content-Length: 12
Connection: close
Content-Type: text/html

Hello world!
"""


def do_request(conn):
    body = []
    p = HttpParser()

    while True:
        data = conn.recv(1024)
        recved = len(data)
        nparsed = p.execute(data, recved)
        assert nparsed == recved
        if not data:
            break
        if p.is_headers_complete():
            logger.debug(p.get_headers())
        if p.is_partial_body():
            logger.debug("is partial body")
            body.append(p.recv_body())
        if p.is_message_complete():
            break
    logger.debug(body)
    conn.sendall(EXAMPLE_RESPONSE)
