# version.py
# coding: utf-8

# version.py
# Initial Copyright (c) esprit

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import base64
import hashlib
import os
import platform
import sys

from module.xmpp import protocol

MAJOR = "0"
MINOR = "1"

BOT_FEATURES = (
    protocol.NS_ACTIVITY,
    protocol.NS_DISCO_INFO,
    protocol.NS_DISCO_ITEMS,
    protocol.NS_MOOD,
    protocol.NS_MUC,
    protocol.NS_VERSION,
    protocol.NS_PING,
    protocol.NS_RECEIPTS,
    protocol.NS_ENTITY_TIME,
    protocol.NS_VCARD
)

identcat = "bot"
identname = "snapi"
identtype = "pc"

appname = "Snapi-Snup"
caps = "https://github.com/alexesprit/snapi-bot"

osinfo = platform.uname()
osname = u"%s %s" % (osinfo[0], osinfo[2])

workdir = os.path.dirname(sys.argv[0])
if not workdir:
    workdir = os.getcwd()
gitdir = os.path.join(workdir, '.git')
sha = os.popen('git --git-dir="%s" rev-parse --short HEAD' % gitdir).read().strip()
if not sha or 'Not a git' in sha:
    sha = '?'
version = u"%s.%s-%s" % (MAJOR, MINOR, sha)

features = "<".join(BOT_FEATURES)
string = u"%s/%s//%s<%s<" % (identcat, identtype, identname, features)
verhash = base64.b64encode(hashlib.sha1(string).digest())

del features
del string
del osinfo
del workdir
del gitdir
del MAJOR
del MINOR
