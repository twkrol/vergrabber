# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol tomek@kingu.pl
"""
Module to grab actual editions & versions of Nginx HTTP Server
"""
import copy
import urllib.request
import re
from datetime import datetime, date
from bs4 import BeautifulSoup
#from software import Softver

product = "Nginx"

def getEditions(template):
	result = []

	template.product = product
	template.ends = date.max
	
	#Looking for releases
	body = urllib.request.urlopen("http://nginx.org/").read()
	soup = BeautifulSoup(body, "html5lib")
	trs = soup.find('table', {"class":"news"}).find_all("tr")

	need_latest = True

	#Looking for two above editions: main and stable
	for tr in trs:
		item = copy.copy(template)									#copy of Softver object

		tds = tr.find_all("td")

		#find release date
		value = tds[0].get_text()
		item.released = datetime.strptime(value, '%Y-%m-%d').date()

		#find version
		value = tds[1].find("a").get_text()
		if 'nginx-' not in value:
			continue
		item.version = value.split("-")[1]
		item.edition = re.search('\d+\.\d+',item.version).group()
		
		#find release type
		value = tds[1].get_text()
		if 'stable version' in value:
			item.stable = True

		if need_latest:
			item.latest = True
			need_latest = False

		if not item.latest and not item.stable:
			continue

		result.append(item)
	
	return result

# if __name__ == "__main__":
    # print(getEditions(Softver()))
