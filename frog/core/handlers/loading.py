#!/usr/bin/env python
# Author: <Chaobin Tang ctang@redhat.com>
from frog.conf import settings
from frog.utils.importlib import import_module


def load_handlers():
    # TODO (ctang) Possibily registering them into one place
    for handler in settings.INSTALLED_HANDLERS:
        import_module(handler)