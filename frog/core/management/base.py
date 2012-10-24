#!/usr/bin/env python
# Author: <Chaobin Tang ctang@redhat.com>


class CommandError(Exception):
    pass

class CommandType(type):

    def __init__(cls, name, bases, attrs):
        # TODO (ctang) Check against command names being shared
        if not hasattr(cls, 'commands_registry'):
            cls.commands_registry = {}
        else:
            cls.commands_registry[name.lower()] = cls

class BaseCommand(object):

    __metaclass__ = CommandType

    arguments = []

    @classmethod
    def make_arguments(cls, *args, **kwargs):
        cls.arguments.append((args, kwargs))

    def __init__(self, parser, commands=(), args=None):
        self.parser = parser
        self.commands = commands
        self.args = args

    def handle(self):
        raise NotImplementedError