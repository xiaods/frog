#!/usr/bin/env python
# Author: <Chaobin Tang ctang@redhat.com>
from frog.contrib.events.handlers.base import BaseJsonEventHandler


def load_handler(event_type):
    '''
    Return None if no handler found.
    '''
    return BaseJsonEventHandler.handler_registry.get(event_type)