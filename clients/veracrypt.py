# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol tomek@kingu.pl
"""
Module to grab actual editions & versions of Mozilla Firefox
"""
import copy
import urllib.request
from urllib.error import URLError
import re
from datetime import datetime, date
from bs4 import BeautifulSoup

product = "VeraCrypt"


def getEditions(template):
	result = []

	template.product = product
	template.ends = date.max
	template.stable = True
	template.latest = False

	# Looking for releases
	try:
		body = urllib.request.urlopen("https://www.veracrypt.fr/en/Downloads.html").read()
	except URLError:
		return result

	soup = BeautifulSoup(body, "html5lib")
	h3 = soup.find("h3")
	#<h3>Latest Stable Release - 1.21 (<span title="07/09/2017 23:00:00 AM">Sunday July 9, 2017</span>)</h3>

	release = h3.get_text().strip().split(" ")[-5]
	tvalue = h3.find('span')['title']

	released = datetime.strptime(tvalue, '%d/%m/%Y %H:%M:%S %p').date()  # date format example: "07/09/2017 23:00:00 AM"
	# One time year fix as there was error on the VeraCrypt title date
	if released.year == 2018:
		released = released.replace(year = released.year + 1)

	# Getting release data
	item = copy.copy(template)  # copy of Softver object

	# find version
	item.version = release

	value = re.search('\d+', release)
	item.edition = value.group()

	# find release date
	item.released = released

	# find release type
	item.latest = True

	result.append(item)

	return result

# if __name__ == "__main__":
# print(getEditions(Softver()))
