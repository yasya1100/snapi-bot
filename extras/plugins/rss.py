# coding: utf-8

# rss.py
# Initial Copyright (с) 2010 -Esprit-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import hashlib

RSSITEMS_FILE = 'rssitems.txt'
RSSCACHE_FILE = 'rsscache.txt'

gRSSItems = {}
gRSSCache = {}

TYPE_RSS = 0x1
TYPE_ATOM = 0x2

RSS_UPDATE_TIME = 1800
RSS_CACHE_SIZE = 30

RSS_SEND_INTERVAL = 10

def loadRSSChannels(conference):
	fileName = getConfigPath(conference, RSSITEMS_FILE)
	utils.createFile(fileName, '{}')
	gRSSItems[conference] = eval(utils.readFile(fileName))

	fileName = getConfigPath(conference, RSSCACHE_FILE)
	utils.createFile(fileName, '{}')
	gRSSCache[conference] = eval(utils.readFile(fileName))

def freeRSSChannels(conference):
	del(gRSSItems[conference])
	del(gRSSCache[conference])

def saveRSSChannels(conference, onlyCache=False):
	if(not onlyCache):
		fileName = getConfigPath(conference, RSSITEMS_FILE)
		utils.writeFile(fileName, str(gRSSItems[conference]))
	
	fileName = getConfigPath(conference, RSSCACHE_FILE)
	utils.writeFile(fileName, str(gRSSCache[conference]))

def cleanRSSCache(conference):
	for url in gRSSCache[conference]:
		cache = gRSSCache[conference][url]
		while(len(cache) > RSS_CACHE_SIZE):
			cache.pop()

def sendRSSNews(conference, url, onlyFirst=False):
	printf("loading %s" % (url))
	rawXML = urllib.urlopen(url).read()
	xmlNode = protocol.simplexml.XML2Node(rawXML)
	if("feed" == xmlNode.getName()):
		rssType = TYPE_ATOM
		itemName = "entry"
		textName = "content"
	else:
		rssType = TYPE_RSS
		itemName = "item"
		textName = "description"
		xmlNode = xmlNode.getFirstChild()
	for i, tag in enumerate(xmlNode.getTags(itemName)):
		name = decode(tag.getTagData("title")).strip()
		tagHash = hashlib.md5(name.encode("utf-8")).hexdigest()
		if(tagHash not in gRSSCache[conference][url]):
			gRSSCache[conference][url].append(tagHash)
			if(not onlyFirst or (onlyFirst and i == 0)):
				text = decode(tag.getTagData(textName)).strip()
				if(TYPE_ATOM == rssType):
					link = decode(tag.getTag("link").getAttr("href")).strip()
				else:
					link = decode(tag.getTagData("link")).strip()
				sendToConference(conference, u"Тема: %s\n%s\n\nСсылка: %s" % (name, text, link))
				time.sleep(RSS_SEND_INTERVAL)
		
def startRSSQuery(conference):
	for url in gRSSItems[conference].values():
		try:
			sendRSSNews(conference, url)
		except:
			pass
	cleanRSSCache(conference)
	saveRSSChannels(conference, True)

def startRSSQueries():
	for conference in getConferences():
		if(gRSSItems[conference]):
			startThread(startRSSQuery, (conference, ))
	startTimer(RSS_UPDATE_TIME, startRSSQueries)

def addRSSChannel(msgType, conference, nick, param):
	param = param.split("=", 1)
	if(2 == len(param)):
		name = param[0].strip()
		url = param[1].strip()
		gRSSItems[conference][name] = url
		gRSSCache[conference][url] = []
		if(name in gRSSItems[conference]):
			sendMsg(msgType, conference, nick, u"добавлено")
		else:
			sendMsg(msgType, conference, nick, u"заменено")
		if(getConfigKey(conference, "rss")):
			sendRSSNews(conference, url, True)
		saveRSSChannels(conference)
	else:
		sendMsg(msgType, conference, nick, u"читай справку по команде")
	
def delRSSChannel(msgType, conference, nick, param):
	if(param in gRSSItems[conference]):
		url = gRSSItems[conference][param]
		del(gRSSItems[conference][param])
		del(gRSSCache[conference][url])
		saveRSSChannels(conference)
		sendMsg(msgType, conference, nick, u"удалено")
	else:
		sendMsg(msgType, conference, nick, u"нет такой ленты")

def showRSSChannels(msgType, conference, nick, param):
	if(not param):
		info = []
		for i, name, in enumerate(gRSSItems[conference]):
			info.append(u"%d) %s" % (i + 1, name))
		if(info):
			message = u"RSS-ленты:\n%s" % (u"\n".join(info))
			sendMsg(msgType, conference, nick, message)
		else:
			sendMsg(msgType, conference, nick, u"нет лент")
	else:
		if(param in gRSSItems[conference]):
			url = gRSSItems[conference][param]
			message = u"Инфо о ленте:\nНазвание: %s\nСсылка: %s" % (param, url)
			sendMsg(msgType, conference, nick, message)
		else:
			sendMsg(msgType, conference, nick, u"нет такой ленты")

registerEvent(startRSSQueries, INIT_2)
registerEvent(loadRSSChannels, ADDCONF)
registerEvent(freeRSSChannels, DELCONF)

registerCommand(addRSSChannel, u"рсс+", 30, \
				u"Добавляет рсс-ленту", u"рсс+ <название = ссылка>", \
				(u"рсс+ "), CHAT | PARAM)
registerCommand(delRSSChannel, u"рсс-", 30, \
				u"Удаляет рсс-ленту", u"рсс- <название>", \
				(u"рсс- новости"), CHAT | PARAM)
registerCommand(showRSSChannels, u"рсс*", 30, \
				u"Показывает рсс-ленты. Если указать название, то выведет подробную информацию", None, \
				(u"рсс*"), CHAT);