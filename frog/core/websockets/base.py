#!/usr/bin/env python
# Author: <Chaobin Tang ctang@redhat.com>
from ws4py.websocket import WebSocket

from frog.core.handlers import dispatch


class ApplicationSocket(WebSocket):
    '''
    A layer on top of ws4py.websocket.
    '''

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.start_application()

    def opened(self):
        '''
        Called when a new connection is established.
        '''
        self.application.opened()

    def closed(self, code, reason=None):
        '''
        Called when the connection is disconnected.
        '''
        self.application.closed(code, reason)

    def received_message(self, message):
        '''
        Called when a message is received. Under the hood this
        could mean that one or more data frames are received
        from the client.
        '''
        self.application.received_message(message)

    def start_application(self):
        '''
        Specify a handler (application) for this connection.
        '''
        application_cls = dispatch(self)
        self.application = application_cls(self)