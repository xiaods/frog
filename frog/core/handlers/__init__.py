#!/usr/bin/env python
# Author: <Chaobin Tang ctang@redhat.com>
from frog.core.handlers.dispatcher import Dispatcher


__all__ = (
    'dispatch',
)


def dispatch(client):
    return Dispatcher.get_handler(client)