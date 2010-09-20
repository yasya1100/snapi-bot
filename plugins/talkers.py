# coding: utf-8;

# talkers.py
# Initial Copyright (c) Gigabyte
# Modification Copyright (c) -Esprit-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

SAVE_COUNT = 20;
TALKERS_FILE = 'talkers.txt';

gTalkers = {};
gMsgCount = {};

def showTopTalkers(msgType, conference, nick):
	base = gTalkers[conference];
	if(base.isEmpty()):
		sendMsg(msgType, conference, nick, u'база болтунов пуста');
	else:
		topList = [];
		replic = u'Статистика топ-участников\nНик, сообщ., /me, слов, слов на сообщ.\n';
		topListLine = u'%d) %s, %d, %d, %d, %0.1f';
		count = 10;
		for jid in base.items():
			statistic = base.getKey(jid);
			words = statistic['words'];
			messages = statistic['messages'];
			meMessages = statistic['mes'];
			userNick = statistic['nick'];
			wordsPerMsg = (float(words)) / (messages + meMessages);
			topList.append([messages, meMessages, words, wordsPerMsg, userNick]);
		topList.sort();
		topList.reverse();
		topList = topList[:10];
		items = [topListLine % (i + 1, x[4], x[0], x[1], x[2], x[3]) for i, x in enumerate(topList)];
		sendMsg(msgType, conference, nick, replic + '\n'.join(items));

def clearStatistic(msgType, conference, nick):
	conference = source[1];
	trueJid = getTrueJid(conference, nick);
	if(getAccess(conference, trueJid) >= 20):
		base = gTalkers[conference];
		base.clear();
		base.save();
		sendMsg(msgType, conference, nick, u'база данных очищена');
	else:
		sendMsg(msgType, conference, nick, u'недостаточно прав');

def showTalkerInfo(msgType, conference, nick, param):
	if(param == u'топ'):
		showTopTalkers(msgType, conference, nick);
	elif(param == u'сброс'):
		clearStatistic(msgType, conference, nick);
	else:
		if(not param):
			trueJid = getTrueJid(conference, nick);
		elif(nickInConference(conference, param)):
			trueJid = getTrueJid(conference, param);
		else:
			return;
		base = gTalkers[conference];
		statistic = base.getKey(trueJid);
		if(statistic):
			statisticLine = u'Статистика для %s\nСообщ.: %d\n/me: %d\nСлов: %d\nСлов на сообщ.: %0.1f';
			words = statistic['words'];
			messages = statistic['messages'];
			meMessages = statistic['mes'];
			nick = statistic['nick'];
			wordsPerMsg = (float(words)) / (messages + meMessages)
			message = statisticLine % (nick, messages, meMessages, words, wordsPerMsg);
			sendMsg(msgType, conference, nick, message);
		else:
			sendMsg(msgType, conference, nick, u'твоя статистика отсутствует');

def updateStatistic(stanza, msgType, conference, nick, trueJid, body):
	if(trueJid != gJid and msgType == PUBLIC and nick):
		base = gTalkers[conference];
		statistic = base.getKey(trueJid);
		if(statistic):
			statistic['nick'] = nick;
		else:
			statistic = {'nick': nick, 'words': 0, 'messages': 0, 'mes': 0};
		if(body.startswith('/me')):
			statistic['mes'] += 1;
		else:
			statistic['messages'] += 1;
		statistic['words'] += len(body.split());
		base.setKey(trueJid, statistic);
		if(gMsgCount[conference] >= SAVE_COUNT):
			base.save();
			gMsgCount[conference] = 0;
		else:
			gMsgCount[conference] += 1;

def loadTalkCache(conference):
	fileName = getConfigPath(conference, TALKERS_FILE);
	gTalkers[conference] = database.DataBase(fileName);
	gMsgCount[conference] = 0;

def unloadTalkCache(conference):
	del(gTalkers[conference]);

registerEvent(loadTalkCache, ADDCONF);
registerEvent(unloadTalkCache, DELCONF);

registerMessageHandler(updateStatistic, CHAT);

registerCommand(showTalkerInfo, u'болтун', 10, u'Показывает статистику болтливости указанного пользователя', u'болтун [ник]', (u'болтун Nick', u'болтун топ'), CHAT);
