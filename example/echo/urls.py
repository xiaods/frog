#!/usr/bin/env python
# Author: <Chaobin Tang ctang@redhat.com>
from frog.contrib.events.handlers.base import JsonEventDispatcherApplication


'''
TODO (ctang) Doing naive things right now here
'''

mappings = {
    '/': JsonEventDispatcherApplication,
}