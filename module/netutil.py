# coding: utf-8

# netutil.py

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import re
import urllib
import urllib2

HTML_ESC_MAP = (
	("&gt;", u">"), 
	("&lt;", u"<"),
	("&apos;", u"'"),
	("&quot;", u"\""),
	("&nbsp;", u" "),
	("&mdash;", u"—"),
	("&middot;", u"·")
)

XML_ESC_MAP = (
	("&gt;", ">"), 
	("&lt;", "<"),
	("&apos;", "'"),
	("&quot;", "\""),
)

HTML_TAG_RE = re.compile(r"<.+?>")

def ustr(text):
	if isinstance(text, unicode):
		return text
	try:
		text = text.__str__()
	except AttributeError:
		text = str(text)
	if not isinstance(text, unicode):
		return unicode(text, "utf-8")
	return text

def unescapeXML(xml):
	for esc, char in XML_ESC_MAP:
		xml = xml.replace(esc, char)
	xml = xml.replace("&amp;", "&")
	return xml

def escapeXML(xml):
	xml = xml.replace("&", "&amp;")
	xml = xml.replace("\x0C", "")
	xml = xml.replace("\x1B", "")
	for esc, char in XML_ESC_MAP:
		xml = xml.replace(char, esc)
	return xml

def unescapeHTML(html):
	for esc, char in HTML_ESC_MAP:
		html = html.replace(esc, char)
	html = html.replace("&amp;", "&")
	return re.sub("&#(\d+);", lambda c: unichr(int(c.group(1))), html)

def decode(text, encoding=None):
	if encoding:
		text = unicode(text, encoding)
	for br in ("<br/>", "<br />", "<br>"):
		text = text.replace(br, "\n")
	text = HTML_TAG_RE.sub("", text)
	return unescapeHTML(text)

def quote(url):
	return urllib.quote(url.encode("utf-8"))
	
def unquote(url):
	return urllib.unquote(url.encode("utf-8"))
	
def getURL(url, param=None, data=None):
	if param:
		query = urllib.urlencode(param)
		url = u"%s?%s" % (url, query)
	if data:
		data = urllib.urlencode(data)
	#url = urllib.quote(url)
	request = urllib2.Request(url, data)
	request.add_header("User-Agent", "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11")
	try:
		return urllib2.urlopen(request)
	except IOError, e:
		print u"Unable to open %s (%s)" % (url, e)
	return None

#USERJID_RE = re.compile(r"\w+@\w+\.\w+", re.UNICODE)
def isJID(jid):
	#if USERJID_RE.search(jid):
	if "@" in jid:
		return True
	return False

#SERVER_RE = re.compile(r"\w+\.\w+", re.UNICODE)
def isServer(server):
	if not server.count(" "):
		#if SERVER_RE.search(server):
		return True
	return False