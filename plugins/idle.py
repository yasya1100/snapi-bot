# coding: utf-8

# idle.py
# Initial Copyright (c) 2007 Als <Als@exploit.in>
# Modification Copyright (c) esprit

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

def showUserIdleTime(msgType, conference, nick, param):
	if isNickOnline(conference, param):
		idleTime = int(time.time() - getNickKey(conference, param, NICK_IDLE))
		if idleTime:
			sendMsg(msgType, conference, nick, u"%s заснул %s назад" % (param, getTimeStr(idleTime)))
		else:
			sendMsg(msgType, conference, nick, u"И что я должна сказать? :)")
	else:
		sendMsg(msgType, conference, nick, u"А это кто?")

registerCommand(showUserIdleTime, u"жив", 10,
				u"Показывает время неактивности пользователя",
				u"<ник>",
				(u"Nick", ),
				CMD_CONFERENCE | CMD_PARAM)
