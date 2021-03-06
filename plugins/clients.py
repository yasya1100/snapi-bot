# coding: utf-8

# clients.py
# Initial Copyright (с) esprit

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

CLIENTS_FILE = "clients.dat"

gUserClients = {}

def loadClientsCache(conference):
	path = getConfigPath(conference, CLIENTS_FILE)
	gUserClients[conference] = database.DataBase(path)

def freeClientsCache(conference):
	del gUserClients[conference]

def showClients(msgType, conference, nick, param):
	userNick = param or nick
	truejid = getTrueJID(conference, userNick)
	if not truejid:
		if netutil.isJID(userNick):
			truejid = userNick
		else:
			sendMsg(msgType, conference, nick, u"А это кто?")
			return
	if truejid in gUserClients[conference]:
		clients = gUserClients[conference][truejid]
		if clients:
			clients.sort()
			if not param:
				message = u"Ты пользуешься следующим: %s" % (u", ".join(clients))
			else:
				message = u"%s пользуется следующим: %s" % (userNick, u", ".join(clients))
			sendMsg(msgType, conference, nick, message)
		else:
			sendMsg(msgType, conference, nick, u"Нет информации")
	else:
		sendMsg(msgType, conference, nick, u"Нет информации")

def saveUserClient(conference, nick, truejid, aff, role):
	base = gUserClients[conference]
	if truejid in base:
		base.updateChangeTime(truejid)
	iq = protocol.Iq(protocol.TYPE_GET)
	iq.setTo(u"%s/%s" % (conference, nick))
	iq.addChild("query", xmlns=protocol.NS_VERSION)
	gClient.sendAndCallForResponse(iq, saveUserClient_, (conference, truejid))

def saveUserClient_(stanza, conference, truejid):
	if protocol.TYPE_RESULT == stanza.getType():
		base = gUserClients[conference]
		query = stanza.getQueryNode()
		if query:
			name = query.getTagData("name")
			if name:
				if truejid not in base:
					base[truejid] = []
				if not name in base[truejid]:
					base[truejid].append(name)
					base.save()

registerEventHandler(loadClientsCache, EVT_ADDCONFERENCE)
registerEventHandler(freeClientsCache, EVT_DELCONFERENCE)

registerEventHandler(saveUserClient, EVT_USERJOIN)

registerCommand(showClients, u"клиенты", 10, 
				u"Показывает названия клиентов, с которых заходил указанный пользователь",
				u"[ник]", 
				(None, u"Niсk"), 
				CMD_CONFERENCE);
