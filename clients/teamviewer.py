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

product = "TeamViewer"


def getReleaseDate(edition):
	# Looking for release date

	# Looking for release's changelog url
	body = urllib.request.urlopen("https://community.teamviewer.com/t5/Change-Log-Windows/bd-p/Change_Log_Windows").read()
	soup = BeautifulSoup(body, "html5lib")
	chlogurl = soup.find("a", href=re.compile(edition))

	# Looking for release date in changelog
	body = urllib.request.urlopen("https://community.teamviewer.com/" + chlogurl['href']).read()
	soup = BeautifulSoup(body, "html5lib")

	value = soup.find("strong", string="Release date:").find_parent()
	value = re.search('\d+\-\d+\-\d+', value.get_text())

	result = datetime.strptime(value.group(), '%Y-%m-%d').date()  # date format example: 2019-03-23

	return result


def getEditions(template):
	result = []

	template.product = product
	template.ends = date.max
	template.stable = True
	template.latest = False

	# Looking for releases
	body = urllib.request.urlopen("https://www.teamviewer.com/en/download/windows/").read()
	soup = BeautifulSoup(body, "html5lib")

	#Windows
	# Looking for tag with content of 3 digits blocks starting with tab eg. <tab>13.2.2344 ...
	found = soup.find(string=re.compile('\t\d+\.\d+\.\d+'))
	release = found.lstrip().rstrip()
	
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
