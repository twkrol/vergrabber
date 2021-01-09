# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol tomek@kingu.pl
"""
Module to grab actual editions & versions of Microsoft Edge
"""
import copy
import urllib.request
import re
from datetime import datetime, date
from bs4 import BeautifulSoup
import logging
from logging import critical, error, info, warning, debug

product = "Microsoft Edge"

def getEditions(template):
    result = []

    template.product = product
    template.ends = date.max
    template.stable = True
    template.latest = True
    
    #Looking for releases
    body = urllib.request.urlopen("https://raw.githubusercontent.com/MicrosoftDocs/Edge-Enterprise/public/edgeenterprise/microsoft-edge-relnote-stable-channel.md").read()
    soup = BeautifulSoup(body, "html5lib")

    for i, string in enumerate(soup.get_text().splitlines()):
        if string.startswith("## Version"):
            # the version line format is: "## Version 87.0.664.66: December 17"
            elements = string.split(' ')
            
            # read version skipping the ending ":"
            releaseVersion = elements[2][:-1]
            
            # decode date, mind the year which is not provided (yet) and must be guessed
            releaseDate = datetime.strptime(f"{elements[3]} {elements[4]}, {datetime.now().year}", '%B %d, %Y')
            if releaseDate.date() > datetime.now().date():
                releaseDate = datetime.strptime(f"{elements[3]} {elements[4]}, {datetime.now().year-1}", '%B %d, %Y')
            
            break
    
    debug(f"version:{releaseVersion}")
    debug(f"releaseDate: {releaseDate}")

    item = copy.copy(template)									#copy of Softver object

    #find release date
    item.released = releaseDate.date()

    #find version
    value = releaseVersion
    item.version = value
    value = re.search('\d+\.\d+',value)
    item.edition = value.group()
    
    result.append(item)

    return result

# if __name__ == "__main__":
    # print(getEditions(Softver()))
