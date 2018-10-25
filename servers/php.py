# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol tomek@kingu.pl
"""
Module to grab actual editions & versions of PHP
"""
import copy
import urllib.request
import re
import json
from datetime import datetime, date
from bs4 import BeautifulSoup
#from software import Softver

product = "PHP"

def getEditions(template):
	result = []
	template.product = product

	#Looking for releases
	body = urllib.request.urlopen("https://secure.php.net/supported-versions.php").read()
	soup = BeautifulSoup(body, "html5lib")
	trs = soup.find("table", {"class":"standard"}).find_next("tbody").find_all("tr")
	
	for tr in trs:

		item = copy.copy(template)											#copy of Softver object
		item.stable = True
		
		#current_date = datetime.utcnow().date()
		
		tds = tr.find_all("td")
				
		#get edition
		item.edition = tds[0].find("a").get_text()
		
		#get EndOfLife
		value = tds[5].get_text()
		item.ends = datetime.strptime(value, '%d %b %Y').date()
				
		#get release date
		value = tds[1].get_text()
		item.released = datetime.strptime(value, '%d %b %Y').date()
								
		result.append(item)
	
	#mark last edition
	result[len(result)-1].latest = True
		
		
	#Looking for legacy releases versions (different url)
	body = urllib.request.urlopen("https://secure.php.net/downloads.php").read()	
	soup = BeautifulSoup(body, "html5lib")
	h3s = soup.find(id="layout-content").find_all("h3", {"class":"title"})
		
	for release in result:
		for h3 in h3s:
			tag = h3["id"]													#full version eg. v7.1.2
			if ("v" + release.edition) in tag:
				patch = tag.split(".")[2]									#keep only last tag number, the patch 
				release.version = release.edition + "." + patch				#apply highest version
		
	return result

# if __name__ == "__main__":
    # print(getEditions(Softver()))
