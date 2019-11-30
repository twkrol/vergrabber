# -*- encoding: utf-8 -*-
# Copyright (c) Florian Probst & Tomasz Krol tomek@kingu.pl
"""
Module to grab the latest "fresh" and "still" versions of LibreOffice for Windows (libreoffice.org)
does not return unstable versions
"""
import copy
import re
import urllib.request
import vergrabber
from bs4 import BeautifulSoup
from datetime import datetime, date

product = "LibreOffice"
user_agent_stable = 'LibreOffice 6.2.1 (c9944f7-48b7ff5-0507789-54a4c8a-8b242a8; Windows; X86_64; )'
user_agent_fresh = 'LibreOffice 6.3.1 (7074905676c47b82bbcfbea1aeefc84afe1c50e1; Windows; X86_64; )'
url = 'http://update.libreoffice.org/check.php'
releases_url = "https://wiki.documentfoundation.org/ReleasePlan/"

"""
get libreoffice webservice output manually:

Stable:
curl -A "LibreOffice 6.2.1 (c9944f7-48b7ff5-0507789-54a4c8a-8b242a8; Windows; X86_64; )" "http://update.libreoffice.org/check.php"
<?xml version="1.0" encoding="utf-8"?>
<inst:description xmlns:inst="http://update.libreoffice.org/description">
  <inst:id>LibreOffice 6.2.7</inst:id>
  <inst:gitid>23edc44b61b830b7d749943e020e96f5a7df63bf</inst:gitid>
  <inst:os>Windows</inst:os>
  <inst:arch>X86_64</inst:arch>
  <inst:version>6.2.7</inst:version>
  <inst:buildid>9999</inst:buildid>
  <inst:update type="text/html" src="https://www.libreoffice.org/download/download/?lang=en-US&amp;version=6.2.7&amp;pk_campaign=update" />
</inst:description>

Fresh:
curl -A "LibreOffice 6.3.1 (7074905676c47b82bbcfbea1aeefc84afe1c50e1; Windows; X86_64; )" "http://update.libreoffice.org/check.php"
<?xml version="1.0" encoding="utf-8"?>
<inst:description xmlns:inst="http://update.libreoffice.org/description">
  <inst:id>LibreOffice 6.3.2</inst:id>
  <inst:gitid>98b30e735bda24bc04ab42594c85f7fd8be07b9c</inst:gitid>
  <inst:os>Windows</inst:os>
  <inst:arch>X86_64</inst:arch>
  <inst:version>6.3.2</inst:version>
  <inst:buildid>9999</inst:buildid>
  <inst:update type="text/html" src="https://www.libreoffice.org/download/download/?lang=en-US&amp;version=6.3.2&amp;pk_campaign=update" />
</inst:description>
"""

def getReleaseDates(item):
    # Looking for release start and end dates
    body = urllib.request.urlopen(releases_url+item.edition).read()
    soup = BeautifulSoup(body, "html5lib")

    # Get all tables from page
    tables = soup.find_all('table')
    for x in range(len(tables)):
        ## tr, (th, td)
        rows = tables[x].find_all('tr')
        # release version info is always in last row
        releaseRow = rows[len(rows)-1]
        ths = releaseRow.find_all('th')
        releaseString = ths[0].get_text()
        tds = releaseRow.find_all('td')
        release_date_string = tds[0].get_text()
        
        #releaseString.
        if releaseString.startswith("Release "+item.version):
            release_match = re.search('([a-zA-Z]{3} \d{1,2}?, \d\d\d\d)', release_date_string)
            if release_match != None:
                release_date_substr = release_match.group(1)
                try:
                    release_date = datetime.strptime(release_date_substr, '%b %d, %Y').date()
                    item.released = release_date
                except ValueError as e:
                     print('ValueError:', e)
            
        if releaseString.startswith("End of"):
            try:
                release_end_date = datetime.strptime(release_date_string, '%B %d, %Y').date()
                item.ends = release_end_date
            except ValueError as e:
                print('ValueError:', e)

def getEditions(template):
    result = []

    template.product = product
    template.ends = date.max

    # Looking for stable release
    request = urllib.request.Request(url, data=None, headers={'User-Agent': user_agent_stable})
    body = urllib.request.urlopen(request).read().decode()
    item = copy.copy(template)  # copy of Softver object    
    regex = re.search('<inst:version>(.*)</inst:version>', str(body))
    if regex != None:
        item.version = regex.group(1)
        minorVersion = re.search('\d+\.\d+',item.version)
        if minorVersion != None:
            item.edition = minorVersion.group()

        item.stable = True
        item.latest = False
        item.released = ""
        getReleaseDates(item)
        result.append(item)
    
    # Looking for fresh release
    request = urllib.request.Request(url, data=None, headers={'User-Agent': user_agent_fresh})
    body = urllib.request.urlopen(request).read().decode()
    item = copy.copy(template)  # copy of Softver object    
    regex = re.search('<inst:version>(.*)</inst:version>', str(body))
    if regex != None:
        item.version = regex.group(1)        
        minorVersion = re.search('\d+\.\d+',item.version)
        if minorVersion != None:
            item.edition = minorVersion.group()
        item.stable = False
        item.latest = True
        item.released = ""
        getReleaseDates(item)
        result.append(item)
        
    return result

if __name__ == "__main__":
    print("LibreOffice Test:")
    libreoffice = getEditions(vergrabber.Softver())
    for x in range(len(libreoffice)):
        print("Version: "+libreoffice[x].version + " from "+str(libreoffice[x].released)+" to "+str(libreoffice[x].ends))
