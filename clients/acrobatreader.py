# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol tomek@kingu.pl & Florian Probst
"""
Module to grab actual editions & versions of Acrobat Reader
"""


import vergrabber
import copy
import urllib.request
import re
from datetime import datetime, date
from bs4 import BeautifulSoup

product = "Adobe Acrobat Reader"
versions_url = "https://helpx.adobe.com/acrobat/release-note/release-notes-acrobat-reader.html"

def getEditions(template):
	result = []

	template.product = product
	template.ends = date.max
	template.stable = True
	template.latest = False

	# Looking for releases
	body = urllib.request.urlopen(versions_url).read()
	soup = BeautifulSoup(body, "html5lib")
	
	# Get all tables from page
	tables = soup.find_all('table')
	for x in range(len(tables)):
		# get all rows (without header)
		rows = tables[x].find_all('tr')[1:]
		# current version is always in the first row
		cols = rows[0].find_all('td')
		release_date_string = cols[0].get_text()
		release = cols[1].get_text()
		# now it should look like this:
		# Date: Feb 21,2019
		# Version: DC Feb 2019 (19.010.20098)
		
		# convert date and version:
		release_match = re.search('\d\d\.\d\d\d.\d+', release)
		if release_match != None:
			release = release_match.group(0)
		elif re.search('\d\d\.\d\.\d+', release) != None:
			release_match = re.search('\d\d\.\d\.\d+', release)
			release = release_match.group(0)
		
		# convert date string to datetime object
		try:
			release_date = datetime.strptime(release_date_string, '%b %d,%Y').date()
		except ValueError as e:
			try:
				release_date = datetime.strptime(release_date_string, '%b %d, %Y').date()
			except ValueError as e:
				print('ValueError:', e)
		
		# now it should look like this:
		# Date:  2019-02-21
		# Version: 19.010.20098
		
		# Fill vergrabber template
		item = copy.copy(template)  # copy of Softver object
		item.version = release
		if release[0:2] != "11":
			item.edition = "DC "+release[0:2]
		else:
			item.edition = "XI"
		if x == 0:
			item.latest = True
		else:
			item.latest = False
		item.released = release_date

		# ignore "XI" version, since it is not supported anymore
		if item.edition != "XI":
			result.append(item)

	return result

if __name__ == "__main__":
	ar = getEditions(vergrabber.Softver())
	for x in range(len(ar)):
		print("Version: "+ar[x].version + " from "+str(ar[x].released))
