# coding: utf-8

# messages.py
# Initial Copyright (с) esprit

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

def sendToAdmins(msgType, conference, nick, param):
	for admin in Config.ADMINS:
		sendTo(protocol.TYPE_PRIVATE, admin, u"Сообщение от %s/%s:\n%s" % (conference, nick, param))
	sendMsg(msgType, conference, nick, u"Ваше сообщение отправлено!")

def messageToChat(msgType, conference, nick, param):
	sendToConference(conference, param)

registerCommand(sendToAdmins, u"мессага_админу", 10,
				u"Отправляет сообщение всем администраторам бота",
				u"<текст>",
				(u"привет!11", ),
				CMD_ANY | CMD_PARAM)
registerCommand(messageToChat, u"сказать", 20,
				u"Сказать через бота в конференции",
				u"<текст>",
				(u"Всем привет!!!", ),
				CMD_CONFERENCE | CMD_PARAM)
