# -*- encoding: utf-8 -*-
# Copyright (c) Florian Probst & Tomasz Krol tomek@kingu.pl
"""
Module to grab the latest stable versions of 7-Zip (7-zip.org)
returns unstable versions (in a separate item) only if they are
newer than the first stable version
"""
import copy
import re
import urllib.request
import vergrabber

from datetime import datetime, date

product = "7-ZIP"
user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46'

def getEditions(template):
	result = []

	template.product = product
	template.ends = date.max
	template.stable = False
	template.latest = False

	# Looking for releases
	url = "https://www.7-zip.org/history.txt"
	request = urllib.request.Request(url, data=None, headers={'User-Agent': user_agent})

	body = urllib.request.urlopen(request).read().decode()
	lines = str(body).splitlines()

	# iterate over all version lines in history.txt to find the first stable version
	versionLines = getVersionLines(lines)
	for x in range(len(versionLines)):
		item = copy.copy(template)  # copy of Softver object	
		version = versionLines[x]
		regex = re.search('^(\d+\.\d+)\s(\D*)\s*(\d\d\d\d-\d\d-\d\d)$', version)
		if regex != None:
			# find version
			item.version = regex.group(1)+" "+regex.group(2)
			item.version = item.version.rstrip()
			item.edition = item.version
			
			# release date
			releaseDate = regex.group(3)
			item.released = datetime.strptime(releaseDate, '%Y-%m-%d').date()  # date format 24-Apr-2018
			
			# set release type
			if x == 0:
				item.latest = True
			
			if len(item.version) <= 5:
				# we found a stable version
				item.stable = True
				result.append(item)
				# return immediately if first stable version has been found
				return result
			result.append(item)
	return result

# fetches all version lines from the history file
def getVersionLines(lines):
	versionLines = []
	for x in range(len(lines)):
		version = lines[x]
		regex = re.search('^(\d+\.\d+)\s(\D*)\s*\d\d\d\d-\d\d-\d\d$', version)
		if regex != None:
			versionLines.append(version)
	return versionLines

if __name__ == "__main__":
	print("7-zip Test:")
	zip7 = getEditions(vergrabber.Softver())
	for x in range(len(zip7)):
		print("Version: "+zip7[x].version + " from "+str(zip7[x].released))

