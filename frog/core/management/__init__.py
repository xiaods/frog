#!/usr/bin/env python
# Author: <Chaobin Tang ctang@redhat.com>
import os
import argparse
import imp

from frog.core.management.base import BaseCommand, CommandError
from frog.core.exceptions import ImproperlyConfigured
from frog.utils.importlib import import_module


_description = """
"""

def find_commands(management_dir):
    """
    Given a path to a management directory, returns a list of all the command
    names that are available.

    Returns an empty list if no commands are defined.
    """
    command_dir = os.path.join(management_dir, 'commands')
    try:
        return [f[:-3] for f in os.listdir(command_dir)
                if not f.startswith('_') and f.endswith('.py')]
    except OSError:
        return []

def load_all_management_commands():
    management_dir = os.path.dirname(__file__)
    command_names = find_commands(management_dir)
    for name in command_names:
        full_name = '%s.%s' % ('frog.core.management.commands', name)
        import_module(full_name)

class CommandUtility(object):

    def __init__(self):
        parser = argparse.ArgumentParser(description=_description)
        
        # command
        parser.add_argument('command',
                            action="store",
                            nargs="+",
                            help="command to execute")
        
        # arguments
        parser.add_argument('--settings', type=str, action='store',
                           help='project settings file')

        # add from all subclasses of BaseCommand the arguments
        for (args, kwargs) in BaseCommand.arguments:
            parser.add_argument(*args, **kwargs)

        self.parser = parser
        self.args = self.parser.parse_args()
        self.commands = getattr(self.args, 'command')

    def get_main_command(self):
        # The last positional argument is the command
        return self.commands[-1]

    def execute(self):
        main_command = self.get_main_command()
        handler_cls = self.load_command_cls(main_command)
        handler_cls(self.parser, self.commands[:-1], self.args).handle()

    def import_command_module(self, command_name):
        '''
        Utilize import_module to import command so
        that it gets interpreted by Python.
        Fail silently.
        '''
        try:
            import_module('frog.core.management.commands.%s' % command_name)
        except ImportError:
            pass

    def load_command_cls(self, command):
        command_cls_registry_name = (command + 'command').lower()
        try:
            return BaseCommand.commands_registry[command_cls_registry_name]
        except KeyError:
            raise CommandError("`%s` is not a valid command." % command)

def import_user_settings():
    try:
        settings_mod_name = os.environ['FROG_SETTINGS_MODULE']
    except KeyError:
        raise ImproperlyConfigured('Variable name `FROG_SETTINGS_MODULE` not defined')
    try:
        settings_mod = import_module(settings_mod_name)
    except ImportError:
        raise ImproperlyConfigured('Settings `%s` not found.' % settings_mod_name)
    return settings_mod

def merge_settings(user_settings):
    '''
    Merge the user-defined settings with frog.conf.settings
    so that all user defined names are available through
    frog.conf.settings.
    '''
    from frog.conf import settings as original_settings
    for name, value in vars(user_settings).iteritems():
        if name.isupper():
            setattr(original_settings, name, value)

def execute_from_terminal():
    load_all_management_commands()
    user_settings = import_user_settings()
    merge_settings(user_settings)
    command = CommandUtility()
    command.execute()