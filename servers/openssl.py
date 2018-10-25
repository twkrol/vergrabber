# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol tomek@kingu.pl
"""
Module to grab actual editions & versions of OpenSSL
"""
import copy
import urllib.request
import re
from datetime import datetime, date
from bs4 import BeautifulSoup
#from software import Softver

product = "OpenSSL"

def getEditions(template):
	result = []
	template.product = product
	template.stable = True
	template.released = date.max
	template.ends = date.min

	#Looking for releases
	body = urllib.request.urlopen("https://www.openssl.org/policies/releasestrat.html").read()
	soup = BeautifulSoup(body, "html5lib")
	li = soup.find('div', {"class" : "entry-content"}).find_next("ul").find_all("li")
	
	for line in li:
		value = line.get_text()

		item = copy.copy(template)											#copy of Softver object
		
		temp = re.search('\d+\.\d+\.\d+',value)
		if temp is not None:
			item.edition = temp.group()
		else:
			continue
		
		temp = re.search('\d+-\d+-.\d+',value)
		if temp is not None:
			item.ends = datetime.strptime(temp.group(), '%Y-%m-%d').date()
		else:
			continue
		
		result.append(item)

		
		
	#Looking for detailed release's versions (different url)
	latest = True															#first found will be marked latest
	body = urllib.request.urlopen("https://www.openssl.org/source/").read()
	soup = BeautifulSoup(body, "html5lib")
	tds = soup.find('div', {"class" : "entry-content"}).find_next("table").find_all("td")
	
	for td in tds:
		value = td.get_text()
		
		#get release date
		temp = re.search('\d{4}-[a-zA-Z]{3}-\d{2}',value)					#Looking for date
		if temp is not None:
			released = datetime.strptime(temp.group(), '%Y-%b-%d').date()
			
		#get version info
		temp = re.search('openssl-(\d+.\d+.\d+[a-z]).tar.gz',value)			#Looking for openssl-x.x.xy release
		if temp is not None:
			version = temp.group(1)
			edition = re.search('\d+.\d+.\d+',version).group()				#Get edition from version
			for item in result:
				if item.edition == edition:
					item.version = version									#Update editions with versions found
					item.stable = True
					item.latest = latest
					item.released = released
					latest = False
		
	return result

# if __name__ == "__main__":
    # print(getEditions(Softver()))
