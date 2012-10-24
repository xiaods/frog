#!/usr/bin/env python
# Author: <Chaobin Tang ctang@redhat.com>

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name = "frog",   
      version = '0.0.1',
      description = "Gevent based websocket application framework for Python",
      maintainer = "Chaobin Tang",
      maintainer_email = "ctang@redhat.com",
      url = "",
      download_url = "",
      packages = ["frog", "frog.core", "frog.core.exceptions", 
                  "frog.handlers", "frog.servers", "frog.websockets"],
      tests_require=['ws4py', 'gevent'],
      test_suite='unittest2.collector',
      platforms = ["any"],
      license = 'BSD',
      long_description = "Gevent based websocket application framework for Python",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Framework :: Gevent',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',   
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: Communications',
          'Topic :: Internet :: WWW/HTTP :: WSGI :: Websocket',
          'Topic :: Software Development :: Libraries :: Python Modules'
          ],
     )