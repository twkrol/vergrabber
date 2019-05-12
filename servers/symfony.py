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
	response = requests.get(url="https://symfony.com/roadmap.json?version=all")
	data = response.json()
	
	editions = data['supported_versions']
	
	for edition in editions:
		item = copy.copy(template)											#copy of Softver object
		item.stable = True
		item.edition = edition

		#Looking for detailed edition information from custom url
		response = requests.get(url="https://symfony.com/roadmap/"+ item.edition +".json")
		data = response.json()

		item.latest = data['is_latest']
		item.released = datetime.strptime(data['release_date'], '%m/%Y').date()
		item.ends = datetime.strptime(data['eom'], '%m/%Y').date()
		item.lts = data['is_lts']

		result.append(item)
		
	#Looking for legacy releases versions (different url)
	body = urllib.request.urlopen("https://api.github.com/repos/symfony/symfony/git/refs/tags").read()	
	data = json.loads(str(body, 'utf-8'))
		
	for release in result:
		max = 0
		clean_edition = release.edition.split(' ')[0]						#remove LTS if part of edition name
		for tags in data:
			tag = tags["ref"].split("/")[2]									#tag eg. v2.3.4
			if ("v" + release.edition) in tag:
				patch = tag.split(".")[2]									#keep only last tag number, the patch 
				num = int(patch) if patch.isdigit() else 0					
				max = num if num > max else max								#finding highest patch number
		release.version = clean_edition + "." + str(max)					#apply highest version

	return result


# if __name__ == "__main__":
    # print(getEditions(Softver()))
