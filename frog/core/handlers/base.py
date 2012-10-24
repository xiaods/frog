#!/usr/bin/env python
# Author: <Chaobin Tang ctang@redhat.com>

__all__ = (
    'WebSocketApplicationType',
    'BaseWebSocketApplication'
)


class WebSocketApplicationType(type):
    '''
    Metaclass for all BaseApplication subclasses.
    '''
    def __init__(cls, name, bases, attrs):
        # TODO (ctang) to check:
        #   - received_message is implemented
        #   - it receives at least one argument, namely `message`
        pass

class BaseWebSocketApplication(object):
    '''
    All application class should subclass this class.
    '''

    __metaclass__ = WebsocketApplicationType

    def __init__(self, connection):
        self.connection = connection

    def run(self):
        pass

    def opened(self):
        raise NotImplementedError

    def closed(self, code, reason=None):
        raise NotImplementedError

    def received_message(self, message):
        raise NotImplementedError

    def response(self, message):
        '''
        Writes data frames to the client.
        '''
        self.connection.send(message)