# coding: utf-8

# stanza.py
# Initial Copyright (c) 2007 dimichxp <dimichxp@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

def sendStanza(msgType, conference, nick, param):
	gClient.send(param)
	sendMessage(msgType, conference, nick, u"Отправлено!")

registerCommand(sendStanza, u"станза", 100, 
				u"Топка", 
				u"<что-то>", 
				(u"</stream:stream>", ), 
				CMD_ANY | CMD_FROZEN | CMD_PARAM)
