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
	maxver = 1507

	# Looking for releases
	body = urllib.request.urlopen("https://winrelinfo.blob.core.windows.net/winrelinfo/en-US.html").read()
	soup = BeautifulSoup(body, "html5lib")
	table = soup.find('table')
	rows = table.find_all('tr')[1:]

	for index, row in enumerate(rows, start=0):  # Python indexes start at zero
		cols = row.find_all('td')

		# Getting release data
		item = copy.copy(template)  # copy of Softver object

		# find release date
		item.released = cols[2].get_text().strip().split('.')[0]

		# find version
		item.version = cols[3].get_text().strip()
		item.edition = cols[0].get_text().strip().split(' ')[0]
		#strip after first 4 chars, as MS adds unusual things there
		item.edition = item.edition[:4]

		# find the latest version (to be set later)
		if int(item.edition) > maxver:
			maxver = int(item.edition)

		result.append(item)

	# mark the latest version
	for item in result:
		if item.edition == str(maxver):
			item.latest = True

	return result

# if __name__ == "__main__":
# print(getEditions(Softver()))
