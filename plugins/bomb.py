# coding: utf-8;

# bomb.py
# Initial Copyright (с) 2010 -Esprit-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

COLORS = (u'красный', u'зеленый', u'черный', u'синий', u'белый', u'желтый', u'серый', u'оранжевый', u'фиолетовый');

gBombColors = {};
gBombAnswer = {};
gBombTimers = {};

def getRandomColors():
	colors = [];
	for color in COLORS:
		if(random.randrange(0, 2)):
			colors.append(color);
	return(colors);

def bombMarked(conference, trueJid):
	return(trueJid in gBombAnswer[conference]);

def giveBomb(msgType, conference, nick, param):
	if(PRIVATE == msgType):
		sendMsg(msgType, conference, nick, u'ага, хочешь без палева кинуть??? ]:->')
		return;
	userNick = param or random.choice(getOnlineNicks(conference));
	if(nickIsOnline(conference, userNick)): 
		trueJid = getTrueJid(conference, userNick);
		if(bombMarked(conference, trueJid)):
			sendMsg(msgType, conference, nick, u'в него уже кинули, ему хватит :-D');
		else:
			colors = getRandomColors();
			gBombAnswer[conference][trueJid] = random.choice(colors);
			gBombColors[conference][trueJid] = colors;
			timeout = random.randrange(40, 71);
			if(colors):
				message = u'вам вручена бомба, на ней %d цветов: %s, ' % (len(colors), ', '.join(colors));
				message += u'выберите цвет провода, который нужно перерезать, бомба взорвется через %s' % (time2str(timeout));
			else:
				# это не баг, это фича :)
				message = u'хаха, тебе не повезло, у тебя бомба БЕЗ проводов! она взорвётся через %s' % (time2str(timeout));
			sendMsg(msgType, conference, userNick, message);
			gBombTimers[conference][trueJid] = startTimer(timeout, bombExec, (msgType, conference, nick, trueJid));
	else:
		sendMsg(msgType, conference, nick, u'а это кто?');			

def bombExec(msgType, conference, nick, trueJid):
	if(nickIsOnline(conference, nick)):
		sendMsg(msgType, conference, nick, u'надо было резать %s, чего тормозишь? :)' % (gBombAnswer[conference][trueJid]));
		detonate(msgType, conference, nick);
	else:
		sendMsg(msgType, conference, nick, u'трус :/');

def bombColorsListener(stanza, msgType, conference, nick, trueJid, param):
	if(bombMarked(conference, trueJid)):
		color = param.lower();
		if(color in gBombColors[conference][trueJid]):
			gBombTimers[conference][trueJid].cancel();
			if(color in gBombAnswer[conference][trueJid]):
				sendMsg(msgType, conference, nick, u'бомба обезврежена!');
			else:
				sendMsg(msgType, conference, nick, u':-| блин, надо было резать %s' % gBombAnswer[conference][trueJid]);
				detonate(msgType, conference, nick);
			del(gBombAnswer[conference][trueJid]);
			del(gBombColors[conference][trueJid]);
			del(gBombTimers[conference][trueJid]);

registerMessageHandler(bombColorsListener, CHAT);

def detonate(msgType, conference, nick):
	num = random.randrange(0, 10);
	if(num < 1 or getNickKey(conference, nick, NICK_MODER)):
		sendMsg(msgType, conference, nick, u'бомба глюкнула...');
	elif(num < 7):
		setRole(conference, nick, ROLE_NONE, u'бабах!!!');
	else:
		setRole(conference, nick, ROLE_VISITOR, u'бабах!!!');
		timeout = random.randrange(100, 501);
		startTimer(timeout, voiceUser, (msgType, conference, nick));

def voiceUser(msgType, conference, nick):
	setRole(conference, nick, ROLE_PARTICIPANT, u'none');

def clearBombCache(conference):
	del(gBombAnswer[conference]);
	del(gBombColors[conference]);
	del(gBombTimers[conference]);	

registerEvent(clearBombCache, DELCONF);

def initBombCache(conference):
	gBombColors[conference] = {};
	gBombAnswer[conference] = {};
	gBombTimers[conference] = {};

registerEvent(initBombCache, ADDCONF);
registerCommand(giveBomb, u'бомба', 15, u'Вручает пользователю бомбу. Если перерезать не тот провод, то будет кик или контузия. Если ник не указан, то берется произвольный ник из чата', u'бомба [ник]', (u'бомба', u'бомба Nick'), CHAT);
