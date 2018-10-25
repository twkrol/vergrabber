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
	# Not implemented yet - lack info on release page
	return date.min


def getEditions(template):
	result = []

	template.product = product
	template.ends = date.max
	template.stable = True
	template.latest = False

	# Looking for releases
	body = urllib.request.urlopen("https://www.teamviewer.com/pl/do-pobrania/windows/").read()
	soup = BeautifulSoup(body, "html5lib")

	#Windows
	# szukamy tagu <p> z treścią rozpoczynającą się od 'v' np. <p>v13.2.2344</p>
	found = soup.find_all("p", string=re.compile('^v'))[0]
	release = found.get_text()[1:]

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
