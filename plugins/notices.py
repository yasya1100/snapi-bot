# coding: utf-8

# notices.py
# Initial Copyright (с) esprit

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

def setDefaultNoticeValue(conference):
	if getConferenceConfigKey(conference, "notices") is None:
		setConferenceConfigKey(conference, "notices", 1)

def manageNoticeValue(msgType, conference, nick, param):
	if param:
		if param.isdigit():
			param = int(param)
			if param == 1:
				setConferenceConfigKey(conference, "notices", 1)
				sendMsg(msgType, conference, nick, u"Оповещения включены")
			else:
				setConferenceConfigKey(conference, "notices", 0)
				sendMsg(msgType, conference, nick, u"Оповещения выключены")
			saveConferenceConfig(conference)
		else:
			sendMsg(msgType, conference, nick, u"Читай помощь по команде")
	else:
		noticesValue = getConferenceConfigKey(conference, "notices")
		sendMsg(msgType, conference, nick, u"Текущее значение: %s" % (noticesValue))

def sendNotices(msgType, conference, nick, param):
	conferences = getConferences()
	if conferences:
		count = 0
		for conf in conferences:
			if getConferenceConfigKey(conf, "notices"):
				sendToConference(conf, u"Новости от администрации:\n%s" % param)
				count += 1
		sendMsg(msgType, conference, nick, 
			"Сообщение ушло в %d конференций из %d" % (count, len(conferences)))
	else:
		sendMsg(msgType, conference, nick, u"Некому рассылать :(")

registerEventHandler(setDefaultNoticeValue, EVT_ADDCONFERENCE)

registerCommand(manageNoticeValue, u"оповещения", 30, 
				u"Отключает (0) или включает (1) сообщения от администраторов бота. Без параметра покажет текущее значение", 
				u"[0|1]", 
				(None, u"0"), 
				CMD_CONFERENCE)
registerCommand(sendNotices, u"оповещение", 100, 
				u"Отправляет сообщение во все конференции, в которых находится бот", 
				u"<текст>", 
				(u"привет!11", ), 
				CMD_ANY | CMD_PARAM)
