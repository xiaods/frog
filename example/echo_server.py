#!/usr/bin/env python
# Author: <Chaobin Tang ctang@redhat.com>
from frog.contrib.events.handlers.base import BaseJsonEventHandler

class EchoEventHandler(BaseJsonEventHandler):

    def proceed(self):
        return {'type': 'reply', 'data': {}}