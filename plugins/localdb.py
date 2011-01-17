# coding: utf-8

# localdb.py
# Initial Copyright (c) 2002-2005 Mike Mintz <mikemintz@gmail.com>
# Modification Copyright (c) 2007 Als <Als@exploit.in>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

LOCALDB_FILE = "localdb.txt"

gLocalBase = {}

def loadLocalBase(conference):
	path = getConfigPath(conference, LOCALDB_FILE)
	gLocalBase[conference] = eval(utils.readFile(path, "{}"))

def saveLocalBase(conference):
	path = getConfigPath(conference, LOCALDB_FILE)
	utils.writeFile(path, str(gLocalBase[conference]))

def freeLocalBase(conference):
	del gLocalBase[conference]

def getLocalKeyToChat(msgType, conference, nick, param):
	key = param.lower()
	if key in gLocalBase[conference]:
		sendMsg(msgType, conference, nick, 
			u"Про %s я знаю следующее:\n%s" % (key, gLocalBase[conference][key]))
	else:
		sendMsg(msgType, conference, nick, u"Я не знаю, что такое %s :(" % (key))

def getLocalKeyToPM(msgType, conference, nick, param):
	args = param.split()
	receiverjid = None
	if len(args) == 2:
		userNick = args[0].strip()
		if isNickOnline(conference, userNick):
			receiverjid = u"%s/%s" % (conference, userNick)
			key = args[1].lower()
	elif len(args) == 1:
		receiverjid = u"%s/%s" % (conference, nick)
		key = args[0].lower()
	if receiverjid:
		if key in gLocalBase[conference]:
			if protocol.TYPE_PUBLIC == msgType:
				sendMsg(msgType, conference, nick, u"Ушло")
			sendTo(protocol.TYPE_PRIVATE, receiverjid, 
				u"Про %s я знаю следующее:\n%s" % (key, gLocalBase[conference][key]))
		else:
			sendMsg(msgType, conference, nick, u"Я не знаю, что такое %s :(" % key)
	else:
		sendMsg(msgType, conference, nick, u"Кому?")

def setLocalKey(msgType, conference, nick, param):
	args = param.split("=", 1)
	if len(args) == 2:
		key = args[0].lower().strip()
		value = args[1].strip()
		if value:
			gLocalBase[conference][key] = u"%s (от %s)" % (value, nick)
			saveLocalBase(conference)
			sendMsg(msgType, conference, nick, u"Буду знать, что такое %s" % (key))
		else:
			if key in gLocalBase[conference]:
				del gLocalBase[conference][key]
				saveLocalBase(conference)
				sendMsg(msgType, conference, nick, u"Прибила %s" % (key))
			else:
				sendMsg(msgType, conference, nick, u"В базе %s и так нету :-P" % (key))
	else:
		sendMsg(msgType, conference, nick, u"Читай помощь по команде")

def searchLocalKey(msgType, conference, nick, param):
	foundElements = []
	for key in gLocalBase[conference].keys():
		if key.count(param):
			foundElements.append(key)
	if foundElements:
		sendMsg(msgType, conference, nick, u"Найдено: %s" % (", ".join(foundElements)))
	else:
		sendMsg(msgType, conference, nick, u"Не найдено!")

def showAllLocalKeysInChat(msgType, conference, nick, param):
	if gLocalBase[conference]:
		message = ", ".join(sorted(gLocalBase[conference].keys()))
		sendMsg(msgType, conference, nick, message)
	else:
		sendMsg(msgType, conference, nick, "База пуста!")

def showAllLocalKeysInPM(msgType, conference, nick, param):
	if gLocalBase[conference]:
		if protocol.TYPE_PUBLIC == msgType:
			sendMsg(msgType, conference, nick, u"Ушли")
		message = ", ".join(sorted(gLocalBase[conference].keys()))
		sendMsg(protocol.TYPE_PRIVATE, conference, nick, message)
	else:
		sendMsg(msgType, conference, nick, "База пуста!")

registerEventHandler(loadLocalBase, EVT_ADDCONFERENCE)
registerEventHandler(freeLocalBase, EVT_DELCONFERENCE)

registerCommand(getLocalKeyToChat, u"???", 10, 
				u"Ищет значение по ключу в локальной базе", 
				u"<ключ>", 
				(u"секрет", ), 
				CMD_CONFERENCE | CMD_PARAM)
registerCommand(getLocalKeyToPM, u"!??", 10, 
				u"Ищет значение по ключу в локальной базе и посылает его в приват. Возможно указание ника отправителя", 
				u"[ник] <ключ>", 
				(u"секрет", u"Nick секрет"), 
				CMD_CONFERENCE | CMD_PARAM)
registerCommand(setLocalKey, u"!!!", 20, 
				u"Устанавливает значение для ключа в локальной базе. Если значение для ключа не указывать, то ключ будет удалён", 
				u"<ключ> = <значение>", 
				(u"секрет =", u"секрет = :-P"), 
				CMD_CONFERENCE | CMD_PARAM)
registerCommand(searchLocalKey, u"???поиск", 10, 
				u"Ищет ключи в локальной базе",
				u"<ключ>", 
				(u"секрет", ), 
				CMD_CONFERENCE | CMD_PARAM)
registerCommand(showAllLocalKeysInChat, u"???все", 10, 
				u"Показывает все ключи локальной базы",
				None, 
				None, 
				CMD_CONFERENCE | CMD_NONPARAM)
registerCommand(showAllLocalKeysInPM, u"!??все", 10, 
				u"Отсылает список ключей локальной базы в приват",
				None, 
				None, 
				CMD_CONFERENCE | CMD_NONPARAM)
