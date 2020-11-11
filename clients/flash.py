# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol tomek@kingu.pl
"""
Module to grab actual editions & versions of Mozilla Firefox
"""
import logging
import copy
import urllib.request
import re
from datetime import datetime, date
from bs4 import BeautifulSoup

product = "Adobe Flash Player"


def getReleaseDate(edition):
	# Looking for release date
	url = "https://helpx.adobe.com/flash-player/release-note/fp_" + edition + "_air_" + edition + "_release_notes.html"
	body = urllib.request.urlopen(url).read()
	logging.debug(url)
	soup = BeautifulSoup(body, "html5lib")
	tree = soup.find('div', {'class': 'text parbase section'})
	for leaf in tree:
		value = leaf.find_next('div').find_next('p').find_next('p').find_next('strong').get_text()
		try:
			result = datetime.strptime(value, '%B %d, %Y').date()  # date format example: March 7, 2017
			return result
		except:
			continue


def getEditions(template):
	result = []

	template.product = product
	template.ends = date.max
	template.stable = True
	template.latest = False

	# Looking for releases
	body = urllib.request.urlopen("https://www.adobe.com/software/flash/about/").read()
	soup = BeautifulSoup(body, "html5lib")
	table = soup.find_all('table')[0]
	rows = table.find_all('tr')[1:]

	for index, row in enumerate(rows, start=0):  # Python indexes start at zero
		cols = row.find_all('td')
		if "rowspan" in cols[0].attrs:
			value = cols[2].get_text()
			if cols[0].get_text() == 'Windows':
				release = value

			# 	versions['Windows'] = value
			# elif cols[0].get_text() == 'MacintoshOS X':
			# 	versions['Osx'] = value
			# elif cols[0].get_text() == 'Linux':
			# 	versions['Linux'] = value

	# Getting release data
	item = copy.copy(template)  # copy of Softver object

	# find version
	item.version = release
	value = re.search('\d+', release)
	item.edition = value.group()

	# find release date
	item.released = getReleaseDate(item.edition)

	# find release type
	item.latest = True

	result.append(item)

	return result

# if __name__ == "__main__":
# print(getEditions(Softver()))
