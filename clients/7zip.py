# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol tomek@kingu.pl
"""
Module to grab actual editions & versions of Mozilla Firefox
"""
import copy
import re
import urllib.request
import vergrabber

from datetime import datetime, date

product = "7-ZIP"
user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46'


def getReleaseDate(version):
    # Looking for release date
    url = "https://www.7-zip.org/history.txt"
    request = urllib.request.Request(url, data=None, headers={'User-Agent': user_agent})
    
    body = urllib.request.urlopen(request).read().decode()
    lines = body.splitlines()
    versionline = getFirstVersionLine(lines)
    regex = re.search('(\d\d\d\d-\d\d-\d\d)$', versionline)  #2019-02-21
    date = regex.group(1)
    result = datetime.strptime(date, '%Y-%m-%d').date()  # date format 24-Apr-2018
    return result


def getEditions(template):
    result = []

    template.product = product
    template.ends = date.max
    template.stable = True
    template.latest = False

    # Looking for releases
    url = "https://www.7-zip.org/history.txt"
    request = urllib.request.Request(url, data=None, headers={'User-Agent': user_agent})

    body = urllib.request.urlopen(request).read().decode()
    lines = str(body).splitlines()

    # Getting release data
    item = copy.copy(template)  # copy of Softver object

    version = getFirstVersionLine(lines)
    regex = re.search('^(\d+\.\d+)\s(\D*)\s*\d\d\d\d-\d\d-\d\d$', version)
    if regex != None:
        # find version
        item.version = regex.group(1)+" "+regex.group(2)
        item.version = item.version.rstrip()
        item.edition = item.version

    # find release date
    item.released = getReleaseDate(version)

    # find release type
    item.latest = True

    result.append(item)

    return result

def getFirstVersionLine(lines):
    for x in range(20):
        version = lines[x]
        regex = re.search('^(\d+\.\d+)\s(\D*)\s*\d\d\d\d-\d\d-\d\d$', version)
        if regex != None:
             return version

if __name__ == "__main__":
    print("7-zip Test:")
    zip7 = getEditions(vergrabber.Softver())
    print("Version: "+zip7[0].version)
    print("Released: "+str(zip7[0].released))

