# -*- encoding: utf-8 -*-
# Copyright (c) Florian Probst & Tomasz Krol tomek@kingu.pl
"""
Module to grab the latest stable versions of LibreOffice for Windows 64 bit (libreoffice.org)
does not return unstable versions
"""
import copy
import re
import urllib.request
import sys
sys.path.insert(1, '/home/obsti/git/vergrabber')
import vergrabber


from datetime import datetime, date

product = "LibreOffice"
user_agent_stable = 'LibreOffice 6.2.1 (c9944f7-48b7ff5-0507789-54a4c8a-8b242a8; Windows; X86_64; )'
user_agent_fresh = 'LibreOffice 6.2.1 (7074905676c47b82bbcfbea1aeefc84afe1c50e1; Windows; X86_64; )'
url = 'http://update.libreoffice.org/check.php'

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
curl -A "LibreOffice 6.2.1 (7074905676c47b82bbcfbea1aeefc84afe1c50e1; Windows; X86_64; )" "http://update.libreoffice.org/check.php"
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

def getEditions(template):
    result = []

    template.product = product
    template.ends = date.max
    template.stable = False
    template.latest = False

    # Looking for stable release
    request = urllib.request.Request(url, data=None, headers={'User-Agent': user_agent_stable})
    body = urllib.request.urlopen(request).read().decode()
    item = copy.copy(template)  # copy of Softver object    
    regex = re.search('<inst:version>(.*)</inst:version>', str(body))
    if regex != None:
        item.version = regex.group(1)
        item.edition = "Still/Stable"
        item.stable = True
        item.latest = False
        item.released = ""
        result.append(item)
    
    # Looking for fresh release
    request = urllib.request.Request(url, data=None, headers={'User-Agent': user_agent_fresh})
    body = urllib.request.urlopen(request).read().decode()
    item2 = copy.copy(template)  # copy of Softver object    
    regex = re.search('<inst:version>(.*)</inst:version>', str(body))
    if regex != None:
        item2.version = regex.group(1)
        item2.edition = "Fresh"
        item2.stable = False
        item2.latest = True
        item2.released = ""
        result.append(item2)
        
    return result

if __name__ == "__main__":
    print("LibreOffice Test:")
    libreoffice = getEditions(vergrabber.Softver())
    for x in range(len(libreoffice)):
        print("Version: "+libreoffice[x].version + " from "+str(libreoffice[x].released))
