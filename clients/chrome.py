# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol tomek@kingu.pl
"""
Module to grab actual editions & versions of Mozilla Firefox
"""
import copy
import requests
import re
from datetime import datetime, date
from bs4 import BeautifulSoup

product = "Google Chrome"

def getEditions(template):
	result = []

	template.product = product
	template.ends = date.max
	template.stable = True
	
	#Looking for releases
	response = requests.get(url="https://omahaproxy.appspot.com/all.json")
	data = response.json()
	
	#Looking releases
	item = copy.copy(template)									#copy of Softver object
	
	for element in data:
		platform = element['os']
		if platform != 'win64':
			continue
		else:
			versions = element['versions']
			for version in versions:
				if version['channel'] != 'stable':
					continue
				else:
					#print(version['channel'])
	
					#find release date
					value = version['current_reldate']
					item.released = datetime.strptime(value, '%m/%d/%y').date()

					#find version
					value = version['version']
					item.version = value
					value = re.search('\d+\.\d+',value)
					if value == None:
						continue
					else:
						item.edition = value.group()
					
					item.latest = True
					
					result.append(item)
	
	return result

# if __name__ == "__main__":
    # print(getEditions(Softver()))
