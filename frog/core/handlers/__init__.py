#!/usr/bin/env python
# Author: <Chaobin Tang ctang@redhat.com>
from frog.core.handlers.dispatcher import Dispatch


__all__ = (
    'dispatch',
)


def dispatch(client):
    return Dispatch.get_handler(client)