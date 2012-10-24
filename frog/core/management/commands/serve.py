#!/usr/bin/env python
# Author: <Chaobin Tang ctang@redhat.com>
from frog.core.management.base import BaseCommand
from frog.core.servers.base import BaseServer
from frog.core.handlers import loading


class ServeCommand(BaseCommand):

    default_addr = "0.0.0.0:9001"

    BaseCommand.make_arguments(
        '--addr',
        type=str,
        action='store',
        default=default_addr,
        help='address to bind to (default: %s)' % default_addr
    )

    def handle(self):
        address = getattr(self.args, 'addr')
        addr, port = address.split(':')
        address = (addr, int(port))
        self.start_server(address)

    def start_server(self, address):
        loading.load_handlers()
        server = BaseServer(address)
        server.serve_forever()