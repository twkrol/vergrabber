# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol tomek@kingu.pl
"""
Module to grab actual editions & versions of TeamViewer
"""
import copy
import urllib.request
import re
from datetime import datetime, date
from bs4 import BeautifulSoup
import logging
from logging import critical, error, info, warning, debug

product = "TeamViewer"
headers = {'User-agent': 'Mozilla/5.0'}	#needed for anti-script scrapping protection


def getReleaseDate(edition):
	# Looking for release date

	# Looking for release's changelog url
	url = "https://community.teamviewer.com/English/categories/change-logs-en"
	req = urllib.request.Request(url, None, headers)

	body = urllib.request.urlopen(req).read()

	soup = BeautifulSoup(body, "html5lib")
	chlogurl = soup.find("a", href=re.compile(edition), string=f"[Windows] v{edition} - Change Log")
	
	debug(f"chlogurl: {chlogurl}")

	# Looking for release date in changelog
	try:
		body = urllib.request.urlopen("https://community.teamviewer.com/" + chlogurl['href']).read()
		soup = BeautifulSoup(body, "html5lib")

		value = soup.find("strong", string="Release date:").find_parent()
		value = re.search('\d+\-\d+\-\d+', value.get_text())

		result = datetime.strptime(value.group(), '%Y-%m-%d').date()  # date format example: 2019-03-23
	except:
		result = date.today()
		
	return result


def getEditions(template):
	result = []

	template.product = product
	template.ends = date.max
	template.stable = True
	template.latest = False

	# Looking for releases
	url = "https://www.teamviewer.com/en/download/windows/"
	request = urllib.request.Request(url, data=None, headers=headers)

	body = urllib.request.urlopen(request).read()
	soup = BeautifulSoup(body, "html5lib")

	#Windows
	# Looking for tag with content of 3 digits blocks starting with tab eg. <tab>13.2.2344 ...
	found = soup.find(string=re.compile('Current version: \d+\.\d+\.\d+'))
	release = found[16:].lstrip().rstrip()
	
	debug(f"release: {release}")

	# Getting release data
	item = copy.copy(template)  # copy of Softver object

	# find version
	item.version = release
	value = re.search('\d+\.\d+', release)
	item.edition = value.group()

	# find release date
	item.released = getReleaseDate(item.version)

	# find release type
	item.latest = True

	result.append(item)

	return result

# if __name__ == "__main__":
# print(getEditions(Softver()))
