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

product = "Java"


def getReleaseDate():
	# Looking for release date
	body = urllib.request.urlopen("https://www.java.com/en/download/faq/release_dates.xml").read()
	soup = BeautifulSoup(body, "html5lib")
	value = soup.find('table', {'class': 'lined'}).find_next('tr').find_next('td').find_next('td').get_text()
	result = datetime.strptime(value, '%B %d, %Y').date()  # date format example: March 7, 2017
	return result


def getEditions(template):
	result = []

	template.product = product
	template.ends = date.max
	template.stable = True
	template.latest = False

	# Looking for releases
	body = urllib.request.urlopen("http://javadl-esd-secure.oracle.com/update/baseline.version").read()
	version = str(body, 'utf-8').split('\n', 1)[1]
	regex = re.search('(\d+)\.(\d+)\.(\d+)_(\d+)', version)

	# Getting release data
	item = copy.copy(template)  # copy of Softver object

	# find version
	item.version = regex.group(2)+'.'+regex.group(3)+'.'+regex.group(4)

	#find edition
	item.edition = regex.group(2)+'.'+regex.group(3)

	# find release date
	item.released = getReleaseDate()

	# find release type
	item.latest = True

	result.append(item)

	return result

# if __name__ == "__main__":
# print(getEditions(Softver()))
