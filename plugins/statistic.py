# coding: utf-8

# statistic.py
# Initial Copyright (с) esprit

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

gConferenceStats = {}
gStatsJoined = {}
gStatsLeaved = {}
gStatsKicked = {}
gStatsBanned = {}

def showConferenceStats(msgType, conference, nick, param):
	buf = []
	buf.append(u"За время, проведённое мной в конфе, вы запостили %(groupchat)d мессаг в чат и %(chat)d мессаг мне в личку, ")
	buf.append(u"я же запостила %(mymsg)d сообщений. Всего сюда заходили %(join)d человек, из них %(moderator)d модеров, ")
	buf.append(u"%(participant)d участников и %(visitor)d посетителей. Вышло же %(leave)d человек; модеры выгнали %(kick)d человек и ")
	buf.append(u"забанили %(ban)d. Также ники сменили %(nick)d раз, статусами нафлудили %(status)d раз.")
	sendMsg(msgType, conference, nick, "".join(buf) % (gConferenceStats[conference]))

def updateBotMessageStats(msgType, conference, text):
	if protocol.TYPE_PUBLIC == msgType and text:
		gConferenceStats[conference]["mymsg"] += 1

def updateMessageStats(stanza, msgType, conference, nick, truejid, text):
	if nick != getBotNick(conference):
		gConferenceStats[conference][msgType] += 1

def updateJoinStats(conference, nick, truejid, aff, role):
	if not truejid in gStatsJoined[conference]:
		gStatsJoined[conference].append(truejid)
		gConferenceStats[conference]["join"] += 1
		gConferenceStats[conference][role] += 1

def updateLeaveStats(conference, nick, truejid, reason, code):
	if not truejid in gStatsLeaved[conference]:
		gStatsLeaved[conference].append(truejid)
		gConferenceStats[conference]["leave"] += 1
	if code == "307" and not truejid in gStatsKicked[conference]:
		gConferenceStats[conference]["kick"] += 1
		gStatsKicked[conference].append(truejid)
	elif code == "301" and not truejid in gStatsBanned[conference]:
		gConferenceStats[conference]["ban"] += 1
		gStatsBanned[conference].append(truejid)

def updatePresenceStats(stanza, conference, nick, truejid):
	stype = stanza.getType()
	if protocol.TYPE_ERROR != stype:
		code = stanza.getStatusCode()
		if "303" == code:
			gConferenceStats[conference]["nick"] += 1
		elif not code:
			if stype != protocol.PRS_OFFLINE:
				gConferenceStats[conference]["status"] += 1
	
def initConferenceStats(conference):
	gConferenceStats[conference] = {
			"nick": 0, 
			"status": 0, 
			"kick": 0, 
			"ban": 0, 
			"join": 0, 
			"leave": 0, 
			"mymsg": 0, 
			protocol.TYPE_PRIVATE: 0, 
			protocol.TYPE_PUBLIC: 0, 
			protocol.ROLE_MODERATOR: 0, 
			protocol.ROLE_PARTICIPANT: 0, 
			protocol.ROLE_VISITOR: 0
	}
	gStatsJoined[conference] = []
	gStatsLeaved[conference] = []
	gStatsKicked[conference] = []
	gStatsBanned[conference] = []

def freeConferenceStats(conference):
	del gConferenceStats[conference]
	del gStatsJoined[conference]
	del gStatsLeaved[conference]
	del gStatsKicked[conference]
	del gStatsBanned[conference]

registerEventHandler(initConferenceStats, EVT_ADDCONFERENCE)
registerEventHandler(freeConferenceStats, EVT_DELCONFERENCE)

registerEventHandler(updateJoinStats, EVT_USERJOIN)
registerEventHandler(updateLeaveStats, EVT_USERLEAVE)

registerEventHandler(updateMessageStats, EVT_MSG | H_CONFERENCE)
registerEventHandler(updatePresenceStats, EVT_PRS | H_CONFERENCE)

registerEventHandler(updateBotMessageStats, EVT_SELFMSG)

registerCommand(showConferenceStats, u"статистика", 10, 
				u"Показывает статистику текущей конференции",
				None, 
				None, 
				CMD_CONFERENCE | CMD_NONPARAM)
