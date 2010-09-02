# coding: utf-8;

# prefix.py
# Initial Copyright (с) 2010 -Esprit-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

CFG_PREFIX = 'prefix';

def prefixControl(msgType, conference, nick, param):
	if(param):
		if(param.lower() != 'none'):
			setConfigKey(conference, CFG_PREFIX, param);
			sendMsg(msgType, conference, nick, u'установлен префикс: %s' % (param));
		else:
			setConfigKey(conference, CFG_PREFIX, None);
			sendMsg(msgType, conference, nick, u'префикс для команд отключен');
		saveChatConfig(conference);
	else:
		sendMsg(msgType, conference, nick, u'текущее значение: %s' % (getConfigKey(conference, CFG_PREFIX)));

def setDefaultPrefix(conference):
	if(getConfigKey(conference, CFG_PREFIX) is None):
		setConfigKey(conference, CFG_PREFIX, None);

registerEvent(setDefaultPrefix, ADDCONF);
registerCommand(prefixControl, u'префикс', 30, u'Устанавливает или отключает (если указать None) префикс для команд. Без параметра покажет текущее значение', u'префикс [что-то]', (u'префикс _', u'префикс None'), CHAT);
