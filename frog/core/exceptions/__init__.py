#!/usr/bin/env python
# Author: <Chaobin Tang ctang@redhat.com>


__all__ = (
    'ApplicationError',
    'HandlerUnavailableError',
    'ImproperlyConfigured'
)


class ImproperlyConfigured(Exception):

    pass

class ApplicationError(Exception):

    pass

class HandlerUnavailableError(Exception):

    pass