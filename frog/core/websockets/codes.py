#!/usr/bin/env python
# Author: <Chaobin Tang ctang@redhat.com>

'''
    Reference: http://tools.ietf.org/html/rfc6455#section-7.4.1

   1000

      1000 indicates a normal closure, meaning that the purpose for
      which the connection was established has been fulfilled.

   1001

      1001 indicates that an endpoint is "going away", such as a server
      going down or a browser having navigated away from a page.

   1002

      1002 indicates that an endpoint is terminating the connection due
      to a protocol error.

   1003

      1003 indicates that an endpoint is terminating the connection
      because it has received a type of data it cannot accept (e.g., an
      endpoint that understands only text data MAY send this if it
      receives a binary message).
'''

NORMAL = 1000
GOING_AWAY = 1001
PROTOCOL_ERR = 1002
DATA_ERR = 1003