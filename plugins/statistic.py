# coding: utf-8;

# statistic.py
# Initial Copyright (с) 2010 -Esprit-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

gStats = {};
gJoined = {};
gLeaved = {};
gKicked = {};
gBanned = {};

def showStatistic(msgType, conference, nick, param):
	text = u'за время, проведённое мной в конфе, вы запостили %(groupchat)d мессаг в чат и %(chat)d мессаг мне в личку, ';
	text += u'я же запостила %(mymsg)d сообщений. Всего сюда заходили %(join)d человек, из них %(moderator)d модеров, ';
	text += u'%(participant)d участников и %(visitor)d посетителей. Вышло же %(leave)d человек; модеры выгнали %(kick)d человек и '
	text += u'забанили %(ban)d. Также ники сменили %(nick)d раз, статусами нафлудили %(status)d раз.';
	sendMsg(msgType, conference, nick, text % (gStats[conference]));

registerCommand(showStatistic, u'статистика', 10, u'Статистика текущей конференции', None, (u'статистика', ), CHAT | NONPARAM);

def botMessageUpdate(msgType, jid, text):
	if(PUBLIC == msgType and text):
		gStats[jid]['mymsg'] += 1;

registerBotMessageHandler(botMessageUpdate);

def messageUpdate(stanza, msgType, conference, nick, trueJid, text):
	if(nick != getBotNick(conference)):
		gStats[conference][msgType] += 1;

registerMessageHandler(messageUpdate, CHAT);

def joinUpdate(conference, nick, trueJid, aff, role):
	if(not trueJid in gJoined[conference]):
		gJoined[conference].append(trueJid);
		gStats[conference]['join'] += 1;
		gStats[conference][role] += 1;

registerJoinHandler(joinUpdate);

def leaveUpdate(conference, nick, trueJid, reason, code):
	if(not trueJid in gLeaved[conference]):
		gLeaved[conference].append(trueJid);
		gStats[conference]['leave'] += 1;
	if(code == '307' and not trueJid in gKicked[conference]):
		gStats[conference]['kick'] += 1;
		gKicked[conference].append(trueJid);
	elif(code == '301' and not trueJid in gBanned[conference]):
		gStats[conference]['ban'] += 1;
		gBanned[conference].append(trueJid);

registerLeaveHandler(leaveUpdate);

def presenceUpdate(stanza, conference, nick, trueJid):
	if(conferenceInList(conference)):
		code = stanza.getStatusCode();
		if(code == '303'):
			gStats[conference]['nick'] += 1;
		else:
			msgType = stanza.getType();
			if(msgType != 'unavailable'):
				gStats[conference]['status'] += 1;

registerPresenceHandler(presenceUpdate, CHAT);
	
def createStatistic(conference):
	gStats[conference] = {'nick': 0, 'status': 0, 'kick': 0, 'ban': 0, PRIVATE: 0, PUBLIC: 0, 'join': 0, 'leave': 0, 'mymsg': 0, ROLE_MODERATOR: 0, ROLE_PARTICIPANT: 0, ROLE_VISITOR: 0};
	gJoined[conference] = [];
	gLeaved[conference] = [];
	gKicked[conference] = [];
	gBanned[conference] = [];

registerEvent(createStatistic, ADDCONF);

def deleteStatistic(conference):
	del(gStats[conference]);
	del(gJoined[conference]);
	del(gLeaved[conference]);
	del(gKicked[conference]);
	del(gBanned[conference]);

registerEvent(deleteStatistic, DELCONF);