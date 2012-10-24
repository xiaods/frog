#!/usr/bin/env python
# Author: <Chaobin Tang ctang@redhat.com>
from ws4py.server import geventserver

from frog.core.websockets.base import ApplicationSocket

class BaseServer(geventserver.WebSocketServer):

    def __init__(self, ADDR, *args, **kwargs):
        super(self.__class__, self).__init__(ADDR, websocket_class=ApplicationSocket, *args, **kwargs)