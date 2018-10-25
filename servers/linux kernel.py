# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol tomek@kingu.pl
"""
Module to grab actual editions & versions of Linux Kernel
"""
import copy
import requests
import re
#import json
from datetime import datetime, date
from bs4 import BeautifulSoup

product = "Linux Kernel"

def getEditions(template):
	result = []

	template.product = product
	template.ends = date.max
	template.stable = True
	
	#Looking for releases
	response = requests.get(url="https://www.kernel.org/releases.json")
	data = response.json()
	
	#Looking releases
	for release in data['releases']:
		item = copy.copy(template)									#copy of Softver object

		#find release date
		value = release['released']['isodate']
		item.released = datetime.strptime(value, '%Y-%m-%d').date()

		#find version
		value = release['version']
		item.version = value
		value = re.search('\d+\.\d+',value)
		if value == None:
			continue
		else:
			item.edition = value.group()
		
		#find release type
		value = release['moniker']
		if value == 'stable':
			item.latest = True
		elif value == 'longterm':
			item.latest = False
		else:
			continue

		result.append(item)
	
	return result

# if __name__ == "__main__":
    # print(getEditions(Softver()))
