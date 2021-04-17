# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol tomek@kingu.pl
"""
Module to grab actual editions & versions of MySQL Server
"""
import copy
import urllib.request
import re
from datetime import datetime, date
from bs4 import BeautifulSoup
from socket import error as SocketError
from socket import error
import errno
import logging
from logging import critical, error, info, warning, debug

product = "MySQL"
headers = {'User-agent': 'Mozilla/5.0'}	#needed for anti-script scrapping protection

def __getMysqlReleaseDate(edition, version):
	req = urllib.request.Request("https://dev.mysql.com/doc/relnotes/mysql/"+edition+"/en/", None, headers)
	try:
		body = urllib.request.urlopen(req).read()
	except error:
		error("Error connecting to dev.mysql.com")
		raise

	soup = BeautifulSoup(body, "html5lib")
	dts = soup.find('dl', {"class": "toc"}).find_all("dt")
	for dt in dts:
		#print("__getMysqlReleaseDate:dt.find:", dt) if debug else None

		a = dt.find("span").find("a").get_text()
		if a.find(version) > 0 :
			value = re.search('\d{4}-\d{2}-\d{2}',a)
			if value:
				return datetime.strptime(value.group(), '%Y-%m-%d').date()
			else:
				#sometimes a release was published but without changelog so we put today instead
				return datetime.now().date()


def getEditions(template):
	result = []

	template.product = product
	template.ends = date.max
	template.stable = True
	template.latest = False
	
	#Looking for latest release
	req = urllib.request.Request("https://dev.mysql.com/downloads/mysql/", None, headers)
	body = urllib.request.urlopen(req).read()
	soup = BeautifulSoup(body, "html5lib")
	h1 = soup.find('div', {"id":"ga"}).find("h1").get_text()
	debug(f"ver string: {h1}")

	item = copy.copy(template)									#copy of Softver object
	item.version = re.search('\d+\.\d+\.\d+', h1).group()
	item.edition = re.search('\d+\.\d+',item.version).group()
	debug(f"version: {item.version}, edition: {item.edition}")

	item.latest = True
	item.released = __getMysqlReleaseDate(item.edition, item.version)
	debug(f"item.released: {item.released}")

	result.append(item)

	#Find link previous GA version
	ga_link = soup.find('a', {"class":"version-link-ga"})['href']
	req = urllib.request.Request("https://dev.mysql.com"+ga_link, None, headers)
	debug(f"ga req url: https://dev.mysql.com{ga_link}")
	body = urllib.request.urlopen(req).read()
	soup = BeautifulSoup(body, "html5lib")
	h1 = soup.find('div', {"id":"ga"}).find("h1").get_text()
	debug(f"ga ver string: {h1}")

	item = copy.copy(template)									#copy of Softver object
	item.version = re.search('\d+\.\d+\.\d+', h1).group()
	item.edition = re.search('\d+\.\d+',item.version).group()
	debug(f"ga version: {item.version}, edition: {item.edition}")

	item.latest = False
	item.released = __getMysqlReleaseDate(item.edition, item.version)
	debug(f"ga item.released: {item.released}")

	result.append(item)
	
	return result

# if __name__ == "__main__":
    # print(getEditions(Softver()))
