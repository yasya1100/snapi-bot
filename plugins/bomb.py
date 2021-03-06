# coding: utf-8

# bomb.py
# Initial Copyright (с) esprit

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

COLORS = (
	u"красный",
	u"зеленый",
	u"черный",
	u"синий",
	u"белый",
	u"желтый",
	u"серый",
	u"оранжевый",
	u"фиолетовый"
)

gBombColors = {}
gBombAnswer = {}
gBombTimers = {}

def getRandomColors():
	colors = []
	for color in COLORS:
		if random.randrange(0, 2):
			colors.append(color)
	return colors

def isUserMined(conference, truejid):
	return truejid in gBombAnswer[conference]

def umnineUser(conference, truejid):
	del gBombAnswer[conference][truejid]
	del gBombColors[conference][truejid]
	del gBombTimers[conference][truejid]

def giveBomb(msgType, conference, nick, param):
	if protocol.TYPE_PRIVATE == msgType:
		sendMsg(msgType, conference, nick, u"Ага, хочешь без палева кинуть??? ]:->")
		return
	userNick = param or random.choice(getOnlineNicks(conference))
	if isNickOnline(conference, userNick):
		truejid = getTrueJID(conference, userNick)
		if isUserMined(conference, truejid):
			sendMsg(msgType, conference, nick, u"В него уже кинули, ему хватит :-D")
		else:
			colors = getRandomColors()
			gBombAnswer[conference][truejid] = random.choice(colors)
			gBombColors[conference][truejid] = colors
			timeout = random.randrange(40, 71)
			if colors:
				message = u"Вам вручена бомба, на ней %d проводов: %s, " % (len(colors), ", ".join(colors))
				message += u"выберите цвет провода, который нужно перерезать, бомба взорвется через %s" % (getTimeStr(timeout))
			else:
				# это не баг, это фича :)
				message = u"Хаха, тебе не повезло, у тебя бомба БЕЗ проводов! Она взорвётся через %s" % (getTimeStr(timeout))
			sendMsg(msgType, conference, userNick, message)
			gBombTimers[conference][truejid] = startTimer(timeout, bombExecute, msgType, conference, userNick, truejid)
	else:
		sendMsg(msgType, conference, nick, u"А это кто?")

def bombExecute(msgType, conference, nick, truejid):
	if isNickOnline(conference, nick):
		sendMsg(msgType, conference, nick,
			u"Надо было резать %s, чего тормозишь? :)" % (gBombAnswer[conference][truejid]))
		bombDetonate(msgType, conference, nick)
	else:
		sendMsg(msgType, conference, nick, u"Трус :/")
	umnineUser(conference, truejid)

def bombColorsListener(stanza, msgType, conference, nick, truejid, param):
	if isUserMined(conference, truejid):
		color = param.lower()
		if color in gBombColors[conference][truejid]:
			gBombTimers[conference][truejid].cancel()
			if color == gBombAnswer[conference][truejid]:
				sendMsg(msgType, conference, nick, u"Бомба обезврежена!")
			else:
				sendMsg(msgType, conference, nick,
					u"Блин :-| надо было резать %s" % gBombAnswer[conference][truejid])
				bombDetonate(msgType, conference, nick)
			umnineUser(conference, truejid)

def bombDetonate(msgType, conference, nick):
	num = random.randrange(0, 10)
	if num < 1 or isNickModerator(conference, nick):
		sendMsg(msgType, conference, nick, u"Бомба глюкнула...")
	elif num < 7:
		setMUCRole(conference, nick, protocol.ROLE_NONE, u"Бабах!!!")
	else:
		setMUCRole(conference, nick, protocol.ROLE_VISITOR, u"Бабах!!!")

		timeout = random.randrange(100, 501)
		startTimer(timeout, setMUCRole, conference, nick, protocol.ROLE_PARTICIPANT)

def initBombCache(conference):
	gBombColors[conference] = {}
	gBombAnswer[conference] = {}
	gBombTimers[conference] = {}

def freeBombCache(conference):
	del gBombAnswer[conference]
	del gBombColors[conference]
	del gBombTimers[conference]


registerEventHandler(initBombCache, EVT_ADDCONFERENCE)
registerEventHandler(freeBombCache, EVT_DELCONFERENCE)

registerEventHandler(bombColorsListener, EVT_MSG | H_CONFERENCE)

registerCommand(giveBomb, u"бомба", 15,
				u"Вручает пользователю бомбу. Если пользователь не обезвредит её, то бот может выкинуть его из конференции или лишить голоса",
				u"[ник]",
				(None, u"Nick"),
				CMD_CONFERENCE)
