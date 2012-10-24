#!/usr/bin/env python
# Author: <Chaobin Tang ctang@redhat.com>
from frog.core.management.base import BaseCommand


class HelpCommand(BaseCommand):

    def handle(self):
        self.parser.print_help()