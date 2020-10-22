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

product = "Microsoft Windows 10"

def getEditions(template):
	result = []

	template.product = product
	template.ends = date.max
	template.stable = True
	template.latest = False
	maxver = date(2015, 7, 29)

	# Looking for releases, source at https://docs.microsoft.com/en-us/windows/windows-10/release-information
	body = urllib.request.urlopen("https://winreleaseinfoprod.blob.core.windows.net/winreleaseinfoprod/en-US.html").read()
	soup = BeautifulSoup(body, "html5lib")
	table = soup.find('div',{"id":"winrelinfo_container"}).find_next('table')
	rows = table.find_all('tr')[1:]

	for index, row in enumerate(rows, start=0):  # Python indexes start at zero
		cols = row.find_all('td')

		# Getting release data
		item = copy.copy(template)  # copy of Softver object

		# find release date
		value = cols[4].get_text().strip()
		item.released = datetime.strptime(value, '%Y-%m-%d').date()

		# find end of service date
		value = cols[5].get_text().strip()
		try:
			item.ends = datetime.strptime(value, '%Y-%m-%d').date()
		except ValueError:
			item.ends = date.min

		# find version
		item.version = cols[3].get_text().strip()
		#strip after first 4 chars, as MS adds unusual things there
		item.edition = cols[0].get_text().strip()[:4]

		# find the latest version (to be set later)
		item.avail = datetime.strptime(cols[2].get_text().strip(), '%Y-%m-%d').date()
		if item.avail > maxver:
			maxver = item.avail

		result.append(item)

	# mark the latest version
	for item in result:
		if item.avail == maxver:
			item.latest = True
		del item.avail

	return result

# if __name__ == "__main__":
# print(getEditions(Softver()))
