# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol tomek@kingu.pl
"""
Module to grab actual editions & versions of Symfony
"""
import copy
import urllib.request
import re
import json
import requests
from datetime import datetime, date

product = "Symfony"

def getEditions(template):
	result = []
	template.product = product

	#Looking for releases
	response = requests.get(url="https://symfony.com/releases.json")
	editions = response.json()["supported_versions"]
	
	for edition in list(editions):
		item = copy.copy(template)											#copy of Softver object
		item.stable = True
		item.edition = edition

		#Looking for detailed edition information from custom url
		response = requests.get(url="https://symfony.com/releases/"+ item.edition +".json")
		data = response.json()

		#Skip development versions
		if not data['is_released']:
			continue

		item.version = data['latest_patch_version']
		item.latest = data['is_latest']
		item.released = datetime.strptime(data['release_date'], '%m/%Y').date()
		item.ends = datetime.strptime(data['eom'], '%m/%Y').date()
		item.lts = data['is_lts']

		result.append(item)

	return result


# if __name__ == "__main__":
    # print(getEditions(Softver()))
