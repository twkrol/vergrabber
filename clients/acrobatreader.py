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
	# only consider first three (others are discontinued versions)
	if len(tables) < 3:
		lenTables = len(tables)
	else:
		lenTables = 3
	for x in range(lenTables):
		# get all rows (without header)
		rows = tables[x].find_all('tr')[1:]
		# current version is always in the first row
		cols = rows[0].find_all('td')
		release_date_string = cols[0].get_text().replace('\n','')
		release = cols[1].get_text()
		# now it should look like this:
		# release_date_string: Feb 21, 2020
		# release: DC Feb 2020 (20.010.20098)
		
		# convert date and version:
		release_match = re.search('\d\d\.\d\d\d.\d+', release)
		if release_match != None:
			release = release_match.group(0)
		elif re.search('\d\d\.\d\.\d+', release) != None:
			release_match = re.search('\d\d\.\d\.\d+', release)
			release = release_match.group(0)
		
		try:
			release_date = datetime.strptime(release_date_string, '%b %d, %Y').date()
		except ValueError as e:
			try:
				release_date = datetime.strptime(release_date_string, '%B %d, %Y').date()
			except ValueError as e:
				print('ValueError:', e)

		# now it should look like this:
		# release_date:  2019-02-21
		
		# Fill vergrabber template
		item = copy.copy(template)  # copy of Softver object
		item.version = release
		if cols[1].get_text()[0:2] == "DC":
			item.edition = "DC 20" + release[0:2]
		else:
			item.edition = "20" + release[0:2]
			
		# assume latest is only first and second table (DC/non-DC version)
		if x == 0 or x == 1:
			item.latest = True
		else:
			item.latest = False
		
		item.released = release_date
		result.append(item)
	return result

if __name__ == "__main__":
	ar = getEditions(vergrabber.Softver())
	for x in range(len(ar)):
		print("Edition: "+ar[x].edition+" Version: "+ar[x].version + " from "+str(ar[x].released)+" latest: "+str(ar[x].latest))
