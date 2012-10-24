#!/usr/bin/env python
# Author: <Chaobin Tang ctang@redhat.com>
from frog.core.handlers.base import BaseWebSocketApplication
from frog.core.exceptions import ImproperlyConfigured


__all__ = (
    'Dispatcher',
)


class Dispatcher(object):

    @classmethod
    def resolve(cls, websocket):
        '''
        Resolve from the urls.py the configured handler class
        for this websocket.
        '''
        # TODO (ctang) add the real work here later
        # looking for a BaseApplication subclass
        # against the websocket.environ['path']
        handler_cls = BaseApplication()
        return handler_cls

    @classmethod
    def get_handler(cls, websocket):
        '''
        Get an instance of the located application class.
        '''
        handler_cls = cls.resolve(websocket)
        if not issubclass(handler_cls, BaseWebSocketApplication):
            raise ImproperlyConfigured("ApplicationSocket.application_class should \
                                            be a subclass of BaseApplication")
        handler = handler_cls(websocket)
        websocket.handler = handler
