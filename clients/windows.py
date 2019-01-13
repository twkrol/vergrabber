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
		value = cols[4].get_text().strip().split('.')[0]
		item.released = datetime.strptime(value, '%m/%d/%Y').date()

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

	# Looking for end support date, source at https://support.microsoft.com/en-ca/help/13853/windows-lifecycle-fact-sheet
	body = urllib.request.urlopen("https://support.microsoft.com/en-ca/help/13853/windows-lifecycle-fact-sheet").read()
	soup = BeautifulSoup(body, "html5lib")
	
	# Data to be found in a script tag used by their angular function, not pure html; we get them all
	script = str(soup.find_all("script"))

	for item in result:
		ver = item.edition	#ex. 1809

		# find the beginning and end of the html'like table contents with version related dates
		start = str(script).find("<td>Windows 10, version %s</td>" % ver)
		end = script.find("</tr>", start)
		extracted =script[start-12:end+5]

		# get table cells then use appropriate cell	containg the end of support date
		found = re.findall(r'<td>(.*?)</td>', extracted)
		if len(found)>0:
			item.ends = datetime.strptime(found[2], '%B %d, %Y').date()

	return result

# if __name__ == "__main__":
# print(getEditions(Softver()))
