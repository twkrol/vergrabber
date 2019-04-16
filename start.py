#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol vergrabber@kingu.pl
"""
Application to scrap and publish actual software versions of different kinds provided by modules
"""
import os
import yaml
import json
from datetime import datetime, date
import vergrabber

__version__ = '3.1.6'
__author__ = 'Tomasz Krol'
__author_email__ = 'vergrabber@kingu.pl'

debug = False
debug_module = None
# debug = True
# debug_module = 'firefox'

def dumper(obj):
    if isinstance(obj, date) or isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    try:
        return obj.toJSON()
    except:
        return obj.__dict__


def applyBranch(result, branch, vergrabber):
    for mod in vergrabber.modules:
        subresult = {}
        for entry in vergrabber.editions:
            if entry.product != mod.product:
                continue
            subresult[entry.edition] = entry
        result[branch][mod.product] = subresult


def applyLatest(result, branch, vergrabber):
    for mod in vergrabber.modules:
        for entry in vergrabber.editions:
            if entry.product != mod.product:
                continue
            if not entry.latest:
                continue
            result[branch][mod.product] = entry


# Application starts here
if __name__ == "__main__":

    print("Vergrabber, a software version grabber", __version__)
    print("(C) 2017-2018 by", __author__, __author_email__, "\n")

    print("- loading configuration from config.yaml")
    with open(os.getcwd() + "/config.yaml", 'r') as confile:
        config = yaml.load(confile)

    outdir = config['files']['outdir']
    outfile = config['files']['outfile']
    webdir = config['files']['webdir']

    # preparing header
    result = {'signature':
        {
            'app': 'vergrabber',
            'version': __version__,
            'author': __author__,
            'notice': 'If there is something broken or could be improved - please email me at ' + __author_email__,
            'updated': datetime.utcnow().date(),
            # 'notice': 'client & server root trees will be removed at the end of 2018; consider migrating your code to new structure'
        },
        'server': {},
        'client': {},
        'latest': {
            'server':{},
            'client':{}
        }
    }

    print("- fetching server's modules")

    # enumerating modules in servers folder
    vergrabber.loadModules('servers', debug_module)
    for mod in vergrabber.modules:
        print("  ", mod.product)
        vergrabber.editions += mod.getEditions(vergrabber.Softver())

    # applying server apps
    applyBranch(result, 'server', vergrabber)
    applyLatest(result['latest'], 'server', vergrabber)

    # debug results
    if debug:
        for soft in vergrabber.editions:
            print(soft.product, soft.edition, "version", soft.version, "released", soft.released,
                  ("Stable" if soft.stable == True else ""),
                  ("Latest" if soft.latest == True else ""))

    print("- fetching client's modules")

    # enumerating modules in clients folder
    vergrabber.loadModules('clients', debug_module)
    for mod in vergrabber.modules:
        print("  ", mod.product)
        vergrabber.editions += mod.getEditions(vergrabber.Softver())

    # applying client apps
    applyBranch(result, 'client', vergrabber)
    applyLatest(result['latest'], 'client', vergrabber)

    # show results
    if debug:
        for soft in vergrabber.editions:
            print(soft.product, soft.edition, "version", soft.version, "released", soft.released,
                  ("Stable" if soft.stable == True else ""),
                  ("Latest" if soft.latest == True else ""))

    # show results
    if debug:
        print(json.dumps(result, default=dumper, indent=4))

    # save output json file locally
    print("- saving json result to file", outdir + outfile)
    with open(outdir + outfile, 'w') as out:
        json.dump(result, out, default=dumper, indent=4)

    # save output json file to webdir
    print("- publishing json result file to", webdir)
    with open(webdir + outfile, 'w') as out:
        json.dump(result, out, default=dumper, indent=4)

    print("* FINISHED *")
