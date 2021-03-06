#!/usr/bin/env python
# Author: <Chaobin Tang ctang@redhat.com>
from ws4py.server import geventserver

from frog.core.websockets.base import ApplicationSocket
from frog.contrib.events.handlers.base import BaseJsonEventHandler, \
                                              JsonEventDispatcherApplication

class EchoEventHandler(BaseJsonEventHandler):

    event_type = "echo"

    def proceed(self, data):
        return {'type': 'reply', 'data': data}

class NewConnectionHandler(BaseJsonEventHandler):

    event_type = "_opened"

    def proceed(self, data):
        print "new connection established"
        return {'type': 'reply', 'data': {'msg': 'welcome'}}