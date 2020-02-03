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

debug = False
product = "MySQL"

headers = {'User-agent': 'Mozilla/5.0'}	#needed for anti-script scrapping protection

def __getMysqlReleaseDate(edition, version):
	req = urllib.request.Request("https://dev.mysql.com/doc/relnotes/mysql/"+edition+"/en/", None, headers)
	try:
		body = urllib.request.urlopen(req).read()
	except error:
		print("Error connecting to dev.mysql.com")
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
	print("ver string:", h1) if debug else None

	item = copy.copy(template)									#copy of Softver object
	item.version = re.search('\d+\.\d+\.\d+', h1).group()
	item.edition = re.search('\d+\.\d+',item.version).group()
	print("version:", item.version, " edition:", item.edition) if debug else None

	item.latest = True
	item.released = __getMysqlReleaseDate(item.edition, item.version)
	print("item.released:", item.released) if debug else None

	result.append(item)

	#Find link to other GA versions
	ga_link = soup.find('a', {"class":"version-link-ga"})['href']
	req = urllib.request.Request("https://dev.mysql.com"+ga_link, None, headers)
	body = urllib.request.urlopen(req).read()
	soup = BeautifulSoup(body, "html5lib")
	options = soup.find('select', {"id":"version-ga"}).find_all('option')
	for option in options:
		version = option.get_text()
	
		item = copy.copy(template)									#copy of Softver object
		item.version = re.search('\d+\.\d+\.\d+', version).group()
		item.edition = re.search('\d+\.\d+',item.version).group()
		print("GA version:", item.version, " edition:", item.edition) if debug else None

		item.released = __getMysqlReleaseDate(item.edition, item.version)
		print("GA item.released:", item.released) if debug else None

		result.append(item)
		
	return result

# if __name__ == "__main__":
    # print(getEditions(Softver()))
