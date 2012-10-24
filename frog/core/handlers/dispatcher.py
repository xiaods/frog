#!/usr/bin/env python
# Author: <Chaobin Tang ctang@redhat.com>
from frog.conf import settings
from frog.core.handlers.base import BaseWebSocketApplication
from frog.core.exceptions import ImproperlyConfigured
from frog.utils.importlib import import_module


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
        urls_module_path = settings.URL_CONF
        try:
            urls_module = import_module(urls_module_path)
        except ImportError:
            raise ImproperlyConfigured("URL_CONF `%s` not found." % urls_module_path)
        websocket_path = websocket.environ['PATH_INFO']
        # TODO (ctang) use more sophisticated lookup method
        app_cls = urls_module.mappings.get(websocket_path, None)
        if app_cls is None:
            raise ImproperlyConfigured("No application found listening for connection to this place `%s`" % websocket_path)
        return app_cls

    @classmethod
    def get_handler(cls, websocket):
        '''
        Get an instance of the located application class.
        '''
        handler_cls = cls.resolve(websocket)
        if not issubclass(handler_cls, BaseWebSocketApplication):
            raise ImproperlyConfigured("ApplicationSocket.application_class should \
                                            be a subclass of BaseApplication")
        return handler_cls
