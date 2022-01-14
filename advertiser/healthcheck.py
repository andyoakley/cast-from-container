import sys
import socket
from http.client import HTTPResponse
import requests
from io import BytesIO

import logging
logging.basicConfig(level=logging.INFO)

class FakeSocket():
    def __init__(self, response_bytes):
        self._file = BytesIO(response_bytes)
    def makefile(self, *args, **kw):
        return self._file

class SSDPResponse(object):
    def __init__(self, response):
        self.location = None
        self.usn = None
        self.st = None

        resp = response.decode()

        # ignore our own messages
        if resp.startswith("M-SEARCH"):
            return 

        r = HTTPResponse(FakeSocket(response))
        r.begin()
        self.location = r.getheader("location")
        self.usn = r.getheader("usn")
        self.st = r.getheader("st")

    def __repr__(self):
        return f"<SSDPResponse({self.location}, {self.st}, {self.usn})>"

def discover(service, timeout=1, retries=1, mx=1):
    group = ("239.255.255.250", 1900)
    message = "\r\n".join([
        'M-SEARCH * HTTP/1.1',
        'HOST: {0}:{1}',
        'MAN: "ssdp:discover"',
        'MX: {mx}',
        'ST: {st}',
	'',''])
    socket.setdefaulttimeout(timeout)
    responses = {}
    for _ in range(retries):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.bind(group)
        sock.sendto(message.format(*group, st=service, mx=mx).encode(), group)
        while True:
            try:
                response = SSDPResponse(sock.recv(1024))
                if response.location:
                    responses[response.location] = response
            except socket.timeout:
                break

    return responses.values()



devices = discover("urn:dial-multiscreen-org:service:dial:1")
if len(devices) == 1:
    try:
        r = requests.get(list(devices)[0].location)
    except requests.exceptions.ConnectionError:
        logging.warning("Health failed. Could not connect")
        sys.exit(2)

    logging.info(f"Health OK. Devices found. {devices}")
    sys.exit(0)
else:
    logging.warning("Healh failed. No devices found.")
    sys.exit(1)

