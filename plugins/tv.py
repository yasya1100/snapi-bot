# coding: utf-8

# tv.py
# Initial Copyright (c) 2007 dimichxp <dimichxp@gmail.com>
# Modification Copyright (c) 2007 Als <Als@exploit.in>
# Modification Copyright (c) 2010 -Esprit-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

TVCODES_FILE = "tvchannels.txt"

TV_CATEGORIES = {
	u"новости": "4",
	u"фильмы": "1,1011",
	u"сериалы": "2,1021",
	u"спорт": "3,30,130,1032",
	u"детям": "5,1051",
	u"досуг": "10,11001",
}

def loadTVChannels():
	global TV_CHANNELS
	path = getFilePath(RESOURCE_DIR, TVCODES_FILE)
	TV_CHANNELS = eval(utils.readFile(path, "utf-8"))

def getTVQuery(channel, flag=None):
	param = {
		"mode": "print",
		"channel": channel
	}
	if flag:
		param["flag"] = flag
	query = urllib.urlencode(param)
	return query

def getTVChannelCode(channelName):
	if channelName.isdigit():
		return channelName
	else:
		for x in TV_CHANNELS:
			if channelName == x.lower():
				return TV_CHANNELS[x]

def getTVForChannel(channelCode):
	url = "http://tv.yandex.ru/?%s" % (getTVQuery(channelCode))
	rawHTML = urllib.urlopen(url).read()
	items = re.findall(r"<div>(.+?)\n", rawHTML)
	if items:
		rawtext = "\n".join(items)
		return decode(rawtext, "utf-8")
	return None

def getTVForCategory(category):
	channels = ",".join(TV_CHANNELS.values())
	url = "http://tv.yandex.ru/?%s" % (getTVQuery(channels, category))

	rawhtml = unicode(urllib.urlopen(url).read(), "utf-8")
	pattern = re.compile(r"<table.+?class=\"channel\".+?>(.+?)</table>", re.DOTALL)
	nameptrn = re.compile(r"<br><b>(.+?)</b><br><br>")
	itemptrn = re.compile(r"<div>(.+?)\n")
	
	program = {}
	channels = []
	message = []

	tables = pattern.findall(rawhtml)
	for table in tables:
		channel = nameptrn.search(table).group(1)
		if channel not in program:
			program[channel] = []
			channels.append(channel)
			program[channel] = "\n".join(itemptrn.findall(table))

	for channel in channels:
		message.append(u"%s:\n%s" % (channel, decode(program[channel])))
	if message:
		return "\n".join(message)
	return None

def showTVProgram(msgType, conference, nick, param):
	param = param.lower()
	if u"каналы" == param:
		if protocol.TYPE_PUBLIC == msgType:
			sendMsg(msgType, conference, nick, u"Ушёл")
		tvList = [u"%s - %s" % (code, name) for name, code in TV_CHANNELS.items()]
		tvList.sort()
		sendMsg(protocol.TYPE_PRIVATE, conference, nick, u"Список каналов:\n%s" % ("\n".join(tvList)))		
	elif u"категории" == param:
		if protocol.TYPE_PUBLIC == msgType:
			sendMsg(msgType, conference, nick, u"Ушли")
		tvCats = [cat for cat in TV_CATEGORIES]
		tvCats.sort()
		sendMsg(protocol.TYPE_PRIVATE, conference, nick, u"Список категорий:\n%s" % (", ".join(tvCats)))
	elif param not in TV_CATEGORIES:
		channelCode = getTVChannelCode(param)
		if channelCode:
			program = getTVForChannel(channelCode)
			if program:
				message = u"Вот, что я нашла:\n%s" % (program)
				sendMsg(msgType, conference, nick, message)
			else:
				sendMsg(msgType, conference, nick, u"На сегодня программы нет")
		else:
			sendMsg(msgType, conference, nick, u"Не знаю такого канала/категории")
	else:
		category = TV_CATEGORIES[param]
		program = getTVForCategory(category)
		if protocol.TYPE_PUBLIC == msgType:
			sendMsg(msgType, conference, nick, u"Ушло")	
		if program:
			message = u"Программа для категории \"%s\":\n%s" % (param, program)
			sendMsg(protocol.TYPE_PRIVATE, conference, nick, message)
		else:
			sendMsg(protocol.TYPE_PRIVATE, conference, nick, u"На сегодня программы для этой категории нет")

registerEvent(loadTVChannels, STARTUP)

registerCommand(showTVProgram, u"тв", 10, 
				u"Показать телепрограму для определённого канала/категории. Параметр \"каналы\" - список каналов, параметр \"категории\" - список категорий", 
				u"тв <канал|номер|категория>", 
				(u"тв 101", u"тв первый", u"тв каналы", u"тв категории"), 
				ANY | PARAM)
