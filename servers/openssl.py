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
	max_ver = 0
	body = urllib.request.urlopen("https://www.openssl.org/source/").read()
	soup = BeautifulSoup(body, "html5lib")
	trs = soup.find('div', {"class" : "entry-content"}).find_next("table").find_all("tr")

	for tr in trs:
		item = copy.copy(template)											#copy of Softver object
		tds = tr.find_all("td")

		raw_date = tds[1].get_text()
		raw_file = tds[2].get_text()
	
		# skip header whis is in ordinary td's instead of th's :(
		if raw_date.rstrip() == "Date":
			continue

		# get release date
		temp_date = re.search('\d{4}-[a-zA-Z]{3}-\d{2}', raw_date)					#Looking for date
		released = datetime.strptime(temp_date.group(), '%Y-%b-%d').date()
	
		# get version info
		temp_ver = re.search('openssl-(\d+.\d+.\d+[a-z]).tar.gz', raw_file)			#Looking for openssl-x.x.xy release

		# skip unregular releases
		if temp_ver is None:
			continue
		
		# get version
		version = temp_ver.group(1)
		
		# ver_num = version.replace(".", "")
		ver_num = int(re.sub("[a-z.]", "", version))
		if ver_num > max_ver:
			max_ver = ver_num

		# get edition
		edition = re.search('\d+.\d+.\d+',version).group()				#Get edition from version

		# fill in the item
		item.edition = edition
		item.version = version									#Update editions with versions found
		item.stable = True
		item.latest = False
		item.released = released
		item.lts = ''

		# print("released:%s, version:%s, edition:%s" % (released, version, edition))
		result.append(item)

		# find and mark latest version
		for item in result:
			ver_num = int(re.sub("[a-z.]", "", item.version))
			if ver_num == max_ver:
				item.latest = True
	
	return result

# if __name__ == "__main__":
    # print(getEditions(Softver()))
