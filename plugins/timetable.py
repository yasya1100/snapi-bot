# coding: utf-8

# timetable.py
# Initial Copyright (с) 2010 -Esprit-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

def getTrainTable(cityFrom, cityTo, dateForward):
	url = "http://rasp.yandex.ru/search"
	qparam = {
		"cityFrom": cityFrom.encode("utf-8"),
		"cityTo": cityTo.encode("utf-8"),
		"dateForward": dateForward.encode("utf-8")
	}
	response = getURL(url, qparam)
	if response:
		rawhtml = response.read()
		rawhtml = unicode(rawhtml, "utf-8")
		elements = re.findall(u"<tr class=\"{(.+?)</tr>", rawhtml, re.DOTALL)
		tableList = []
		for element in elements:
			trainName = re.search("<a href=\".+?>(.+?)</a>", element, re.DOTALL)
			trainName = decode(trainName.group(1)).strip()

			dispatch, arrive = re.findall(r"<span class=\"point\">(.+?)</span>", element, re.DOTALL)
			
			timePtrn = re.compile(r"<strong(.+?)</strong>")
			namePtrn = re.compile(r"<a href=\".+?>(.+?)</a>", re.DOTALL)

			disTime = timePtrn.search(dispatch)
			disTime = decode(disTime.group(0)).strip()
			disName = namePtrn.search(dispatch)
			disName = decode(disName.group(1)).strip()
			
			arrTime = timePtrn.search(arrive)
			arrTime = decode(arrTime.group(0)).strip()
			arrName = namePtrn.search(arrive)
			arrName = decode(arrName.group(1)).strip()
			
			travelTime = re.search(r"td class=\"{raw:.+?>.+?</i>(.+?)</td>", element, re.DOTALL)
			travelTime = decode(travelTime.group(1)).strip()

			if element.find("tickets\": \"yes") != -1:
				places = u"есть"
			else:
				places = u"нет"
			tableList.append([trainName, disTime, disName, arrTime, arrName, travelTime, places])
		return tableList
	else:
		return None

def showTrainTable(msgType, conference, nick, param):
	param = param.split(None, 1)
	if len(param) == 2:
		cities = param[1]
		if cities.count(">"):
			cityFrom, cityTo = cities.split(">")
			date = param[0]
			tableList = getTrainTable(cityFrom, cityTo, date)
			message = []
			msgText = u"%d) %s\nВремя отправления: %s (%s)\nВремя прибытия: %s (%s)\nВремя в пути: %s\nМеста: %s"
			if tableList:
				for i, table in enumerate(tableList):
					message.append(msgText % (i + 1, table[0], table[1], table[2], table[3], table[4], table[5], table[6]))
				if protocol.TYPE_PUBLIC == msgType:
					sendMsg(msgType, conference, nick, u"ушло")
				sendMsg(protocol.TYPE_PRIVATE, conference, nick, "\n".join(message))
			else:
				sendMsg(msgType, conference, nick, u"Не найдено!")
		else:
			sendMsg(msgType, conference, nick, u"Читай помощь по команде")

registerCommand(showTrainTable, u"расписание", 10, 
				u"Расписание поездов", 
				u"<дата> <место_отправления > место прибытия>", 
				(u"12.09 Котлас > Ярославль", ), 
				CMD_ANY | CMD_PARAM)
