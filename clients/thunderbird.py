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

product = "Mozilla Thunderbird"
user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46'


def getReleaseDate(version):
	# Looking for release date
	url = "https://www.thunderbird.net/en-US/thunderbird/" + version + "/releasenotes/"
	request = urllib.request.Request(url, data=None, headers={'User-Agent': user_agent})

	body = urllib.request.urlopen(request).read()
	soup = BeautifulSoup(body, "html5lib")
	# value = soup.find('article', {'id': 'main-content'}).find_next('h2').get_text()
	value = soup.find(id='masthead').find_all('section')[1].find('p').text
	value = value[value.rfind(' on ')+4:].strip()
	result = datetime.strptime(value, '%B %d, %Y').date()  # date format example: March 7, 2017
	return result


def getEditions(template):
	result = []

	template.product = product
	template.ends = date.max
	template.stable = True
	template.latest = False

	# Looking for releases
	url = "https://www.thunderbird.net/en-US/thunderbird/releases/"
	request = urllib.request.Request(url, data=None, headers={'User-Agent': user_agent})

	body = urllib.request.urlopen(request).read()
	soup = BeautifulSoup(body, "html5lib")
	items = soup.main.find_all("section")[2].aside.aside.find_all("a")

	release = items[-1].text

	# Getting release data
	item = copy.copy(template)  # copy of Softver object

	# find release date
	item.released = getReleaseDate(release)

	# find version
	item.version = release
	value = re.search('\d+\.\d+', release)
	item.edition = value.group()

	# find release type
	item.latest = True

	result.append(item)

	return result

# if __name__ == "__main__":
# print(getEditions(Softver()))
