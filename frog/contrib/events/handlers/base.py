#!/usr/bin/env python
# Author: <Chaobin Tang ctang@redhat.com>
import cjson

from ws4py.messaging import TextMessage

from frog.core.handlers.base import BaseWebSocketApplication
from frog.core.handlers import loading
from frog.core.websockets import codes


class JsonEventHandlerType(type):
    '''
    Metaclass for all BaseJsonEventHandler subclasses.
    '''

    def __init__(cls, name, bases, attrs):
        # register all handlers
        cls.register_handler(name, bases, attrs)

    def register_handler(cls, name, bases, attrs):
        '''
        Register all subclass of BaseJsonEventHandler in a
        dictionary for quick lookup.
        '''
        if not hasattr(cls, 'event_type'):
            raise TypeError("BaseJsonEventHandler subclasses should have a class \
                            attribute named 'event_type'")
        if not hasattr(cls, 'handler_registry'):
            cls.handler_registry = {}
        else:
            handler_with_same_event_type = cls.handler_registry.get(cls.event_type, None)
            if handler_with_same_event_type:
                raise RuntimeError("`%s` and `%s` are sharing the same event_type `%s`" % (
                    handler_with_same_event_type.__name__, name, cls.event_type
                ))
            handler_implementation = attrs.get('proceed', None)
            if not callable(handler_implementation):
                raise RuntimeError("Event handlers should provide an implementation of `proceed()`")
            if not cls.event_type: # TODO (ctang) More sanity checks probably
                cls.handler_registry[cls.event_type] = cls

class BaseJsonEventHandler(object):
    '''
    All json event handlers should subclass from this class.
    '''

    __metaclass__ = JsonEventHandlerType

    event_type = None

    def __init__(self, websocket, event_data):
        self.websocket = websocket
        self.event_data = event_data

    def proceed(self):
        '''
        All BaseJsonEventHandler subclass should implement this function.
        - return: json, the `event` message to be sent to the client.
        '''
        raise NotImplementedError

class JsonEventDispatcherApplication(BaseWebSocketApplication):
    '''
    Messages sent and received by both server and client should
    look like this,
    
    {
        'type': "event_type",
        'data': {
            'id': some_id,
            'nodes': []
        }
    }
    
    The data is pickled from string to json and encoded
    using UTF-8.
    '''
    # Built-In event types are not allowed to use.
    builtin_events = ('_opened', '_closed')

    def to_json(self, message):
        return cjson.decode(message)

    def to_string(self, data):
        return cjson.encode(data)

    def opened(self):
        opened_event = {
            'type': '_opened',
            'data': {}
        }
        self.dispatch_event(opened_event)

    def closed(self, code, reason=None):
        closed_event = {
            'type': '_closed',
            'data': {
                'code': code,
                'reason': reason
            }
        }
        self.dispatch_event(closed_event)

    def received_message(self, message):
        if not issubclass(message, TextMessage):
            raise TypeError("Not supported message type `%s`." % type(message))
        try:
            event = self.string_to_json(str(message)) # TextMessage type
        except cjson.DecodeError, e:
            self.connection.close(code=codes.DATA_ERR, reason="This is not a valid json data structure.")
        else:
            json = self.dispatch_event(event)
            encoded_json = self.to_string(json)
            self.response(encoded_json)

    def dispatch_event(self, event, *args, **kwargs):
        '''
        This function should always return an `event` in json.
        '''
        event_type = event['type']
        if event_type in self.builtin_events:
            self.connection.close(codes.GOING_AWAY, reason='Builtin event types are not allowed to use.')
        else:
            data = event['data']
            handler_cls = loading.get_handler(event_type)
            if handler_cls:
                # TODO (ctang) Passing in a websocket isn't a good idea, fix later.
                handler = handler_cls(self.connection, data, *args, **kwargs)
                return handler.proceed()
            else:
                self.connection.close(codes.GOING_AWAY, reason='No handler for event type "%s"' % event_type)