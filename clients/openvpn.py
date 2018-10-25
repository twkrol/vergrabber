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

product = "OpenVPN"
user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46'


def getReleaseDate(version):
	# Looking for release date
	url = "http://build.openvpn.net/downloads/releases/latest/"
	body = urllib.request.urlopen(url).read()

	soup = BeautifulSoup(body, "html5lib")
	value = soup.find('a', href='openvpn-install-latest-stable.exe').next_sibling.strip().split(" ")[0]
	result = datetime.strptime(value, '%d-%b-%Y').date()  # date format 24-Apr-2018
	return result


def getEditions(template):
	result = []

	template.product = product
	template.ends = date.max
	template.stable = True
	template.latest = False

	# Looking for releases
	url = "http://build.openvpn.net/downloads/releases/latest/LATEST.txt"
	request = urllib.request.Request(url, data=None, headers={'User-Agent': user_agent})

	body = urllib.request.urlopen(request).read()
	# body = urllib.request.urlopen("http://build.openvpn.net/downloads/releases/latest/LATEST.txt").read()
	firstline = str(body, 'utf-8').split('\n', 1)[0]
	version = firstline.split(':')[1].strip()

	# Getting release data
	item = copy.copy(template)  # copy of Softver object

	# find version
	item.version = version

	#find edition
	value = re.search('\d+\.\d+', version)
	item.edition = value.group()

	# find release date
	item.released = getReleaseDate(version)

	# find release type
	item.latest = True

	result.append(item)

	return result
