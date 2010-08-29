# coding: utf-8;

# users.py
# Initial Copyright (с) 2010 -Esprit-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

def createNickList(nickList):
	items = [u'%d) %s' % (i + 1, ', '.join(nickList[jid])) for i, jid in enumerate(nickList)];
	return('\n'.join(items));
	
def getInMucList(conference, offline = False):
	nicks = (offline) and getNicks(conference) or getOnlineNicks(conference);
	nickList = {};
	for nick in nicks:
		trueJid = getTrueJid(conference, nick);
		if(not trueJid in nickList):
			nickList[trueJid] = [];
		nickList[trueJid].append(nick);
	return(nickList);

def showInMucUsers(type, conference, nick, param):
	nickList = getInMucList(conference);
	text = u'я вижу здесь %d человек:\n' % (len(nickList));
	text += createNickList(nickList);
	sendMsg(type, conference, nick, text);
	
registerCommand(showInMucUsers, u'инмук', 10, u'Показывает список участников, находящихся в конференции', None, (u'инмук', ), CHAT | NONPARAM);

def showWhoWas(type, conference, nick, param):
	nickList = getInMucList(conference, True);
	text = u'я видела здесь %d человек:\n' % (len(nickList));
	text += createNickList(nickList);
	sendMsg(type, conference, nick, text);

registerCommand(showWhoWas, u'хтобыл', 10, u'Показывает список участников, посетивших конференцию за сессию', None, (u'хтобыл', ), CHAT | NONPARAM);
	
def showUserNicks(type, conference, nick, param):
	userNick = param or nick;
	if(nickInConference(conference, userNick)):
		trueJid = getTrueJid(conference, userNick);
		nickList = getInMucList(conference, True);
		nicks = nickList[trueJid];
		if(len(nicks) < 2):
			if(param):
				sendMsg(type, conference, nick, u'не видела, чтобы ' + userNick + u' менял ник');
			else:
				sendMsg(type, conference, nick, u'не видела, чтобы ты менял ник');
		else:
			if(param):
				sendMsg(type, conference, nick, u'%s известен как %s' % (userNick, ', '.join(nicks)));
			else:
				sendMsg(type, conference, nick, u'ты известен как %s' % (', '.join(nicks)));

registerCommand(showUserNicks, u'ники', 10, u'Выводит все ники пользователя', u'ники [ник]', (u'ники', u'ники Nick'), CHAT | NONPARAM);
