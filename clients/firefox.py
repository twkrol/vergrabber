# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol tomek@kingu.pl
"""
Module to grab actual editions & versions of Mozilla Firefox
"""
import copy
import urllib.request
import re
from datetime import datetime, date
from bs4 import BeautifulSoup

product = "Mozilla Firefox"

def getReleaseDate(version):
	#Looking for release date
	body = urllib.request.urlopen("https://www.mozilla.org/en-US/firefox/"+version+"/releasenotes/").read()
	soup = BeautifulSoup(body, "html5lib")
	# value = soup.find('div', {'class':'c-release-version'}).find_next('p').get_text()
	value = soup.find('p', {'class':'c-release-date'}).get_text()
	result = datetime.strptime(value, '%B %d, %Y').date()			#date format example: March 7, 2017
	return result


def getEditions(template):
	result = []

	template.product = product
	template.ends = date.max
	template.stable = True
	template.latest = False
	
	#Looking for releases
	body = urllib.request.urlopen("https://www.mozilla.org/en-US/firefox/releases/").read()
	soup = BeautifulSoup(body, "html5lib")
	html = soup.find('html', dir='ltr')
	lastest_firefox = html['data-latest-firefox']
	esr_versions = html['data-esr-versions']	

	# latest might not be esr - check for this
	if lastest_firefox not in esr_versions:
		esr_versions += ' '+lastest_firefox

	#Looking releases
	for release in esr_versions.split(" "):
		item = copy.copy(template)									#copy of Softver object

		#find release date
		item.released = getReleaseDate(release)

		#find version
		value = release
		item.version = value
		value = re.search('\d+\.\d+',value)
		if value == None:
			continue
		else:
			item.edition = value.group()
		
		#find release type
		value = item.version
		if value == lastest_firefox:
			item.latest = True

		result.append(item)
	
	return result

# if __name__ == "__main__":
    # print(getEditions(Softver()))
