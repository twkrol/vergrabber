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
    body = urllib.request.urlopen("https://docs.microsoft.com/en-us/deployedge/microsoft-edge-relnote-stable-channel").read()
    soup = BeautifulSoup(body, "html5lib")

    for item in soup.find_all('h2'):
        contents = item.get_text()
        if contents.startswith("Version"):
            # the version line format is: "Version 89.0.774.48: March 8"
            elements = contents.split(' ')
            
            # read version skipping the ending ":"
            releaseVersion = elements[1][:-1]

            # decode date, mind the year which is not provided (yet) and must be guessed
            releaseDate = datetime.strptime(f"{elements[2]} {elements[3]}, {datetime.now().year}", '%B %d, %Y')
            if releaseDate.date() > datetime.now().date():
                releaseDate = datetime.strptime(f"{elements[2]} {elements[3]}, {datetime.now().year-1}", '%B %d, %Y')
            
            debug(f"version:{releaseVersion}")
            debug(f"releaseDate: {releaseDate}")

            item = copy.copy(template)									#copy of Softver object

            #find release date
            item.released = releaseDate.date()

            #find version
            value = releaseVersion
            item.version = value
            value = re.search('\d+',value)
            item.edition = value.group()
            
            result.append(item)
            
            # today, we're not interested in older releases
            break

    return result

# if __name__ == "__main__":
    # print(getEditions(Softver()))
