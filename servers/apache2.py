# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol tomek@kingu.pl
"""
Module to grab actual editions & versions of Apache HTTP Server
"""
import copy
import urllib.request
import re
from datetime import datetime, date
from bs4 import BeautifulSoup
#from software import Softver

product = "Apache2"

def getEditions(template):
	result = []

	template.product = product
	template.ends = date.max
	
	#Looking for LATEST STABLE release
	item = copy.copy(template)									#copy of Softver object
	item.stable = True
	item.latest = True

	#Looking for releases
	url = "http://httpd.apache.org/download.cgi"
	req = urllib.request.Request(url, data=None, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'})
	page = urllib.request.urlopen(req)

	soup = BeautifulSoup(page.read(), "html5lib")

	#Check if we got suggested mirror redirect page, if so, reload and next time should be proper download page
	title = soup.find('title').get_text()
	if title == 'Apache Download Mirrors':
		page = urllib.request.urlopen(req)
		soup = BeautifulSoup(page.read(), "html5lib")

	p = soup.find('p', text="Stable Release - Latest Version:")

	li = p.find_next("ul").find_next("li")
	a = li.find("a")
	item.version = a.get_text()
	item.edition = re.search('\d+\.\d+',item.version).group()
		
	value = re.search('(\d{4})[/.-](\d{2})[/.-](\d{2})',li.get_text()).group()
	item.released = datetime.strptime(value, '%Y-%m-%d').date()

	result.append(item)
			
	return result

# if __name__ == "__main__":
    # print(getEditions(Softver()))
