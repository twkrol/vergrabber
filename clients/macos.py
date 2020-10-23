# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol tomek@kingu.pl
"""
Module to grab actual editions & versions of MacOS
"""
from copy import copy
import urllib.request
import re
from datetime import datetime, date
from bs4 import BeautifulSoup
from unidecode import unidecode

product = "Apple Mac"

def getEditions(template):
	result = []

	template.product = product
	template.released = date.min
	template.ends = date.max
	template.stable = True
	template.latest = False
	maxver = None

	# Looking for releases, source at https://docs.microsoft.com/en-us/windows/windows-10/release-information
	body = urllib.request.urlopen("https://support.apple.com/pl-pl/HT201260").read()
	soup = BeautifulSoup(body, "html5lib")
	table = soup.find('div',{"id":"tableWraper"}).find_next('table')
	rows = table.find_all('tr')[1:]

	for index, row in enumerate(rows, start=0):  # Python indexes start at zero

		# copy of Softver object
		item = copy(template)  # copy of Softver object

		# find elements to parse
		cols = row.find_all('td')

		# find product name
		# item.edition = cols[0].get_text().strip().replace('\u00a0', ' ')
		item.edition = unidecode(cols[0].get_text().strip())

		# find version
		item.version = cols[1].get_text().strip()
		
		# mark the latest version
		if maxver is None:
			maxver = item.version
			item.latest = True

		result.append(item)
	return result

# if __name__ == "__main__":
# print(getEditions(Softver()))
