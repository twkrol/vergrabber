#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol vergrabber@kingu.pl
"""
Application to scrap and publish actual software versions of different kinds provided by modules
"""
import sys
import os
import yaml
import json
from datetime import datetime, date
import logging
from logging import critical, error, info, warning, debug
import argparse
import vergrabber

__version__ = '4.2.3'
__author__ = 'Tomasz Krol'
__author_email__ = 'vergrabber@kingu.pl'

debug_module = None

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


def main():
    print(f"Vergrabber, a software version grabber {__version__}")
    print(f"(C) 2017-2020 by {__author__}, {__author_email__}\n")

    started = datetime.now()
    info(f"* STARTED @ {started}")
    info(f"- loading configuration from config.yaml")

    # loading configuration
    with open(os.getcwd() + "/config.yaml", 'r') as confile:
        config = yaml.full_load(confile)

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

    info("- fetching server's modules")

    # enumerating modules in servers folder
    vergrabber.loadModules('servers', debug_module)
    for mod in vergrabber.modules:
        print("  ", mod.product)
        vergrabber.editions += mod.getEditions(vergrabber.Softver())

    # applying server apps
    applyBranch(result, 'server', vergrabber)
    applyLatest(result['latest'], 'server', vergrabber)

    # debug results
    if debug_module:
        for soft in vergrabber.editions:
            debug(f"{soft.product}, {soft.edition}, version {soft.version}, released {soft.released} {('Stable' if soft.stable == True else '')} {('Latest' if soft.latest == True else '')}")

    info("- fetching client's modules")

    # enumerating modules in clients folder
    vergrabber.loadModules('clients', debug_module)
    for mod in vergrabber.modules:
        print("  ", mod.product)
        vergrabber.editions += mod.getEditions(vergrabber.Softver())

    # applying client apps
    applyBranch(result, 'client', vergrabber)
    applyLatest(result['latest'], 'client', vergrabber)

    # show results
    if debug_module:
        for soft in vergrabber.editions:
            debug(f"{soft.product}, {soft.edition}, version {soft.version}, released {soft.released} {('Stable' if soft.stable == True else '')} {('Latest' if soft.latest == True else '')}")

    # show results
    debug(json.dumps(result, default=dumper, indent=4))

    # save output json file locally
    info(f"- saving json result to file {outdir + outfile}")
    with open(outdir + outfile, 'w') as out:
        json.dump(result, out, default=dumper, indent=4)

    # save output json file to webdir
    info(f"- publishing json result file to {webdir}")
    with open(webdir + outfile, 'w') as out:
        json.dump(result, out, default=dumper, indent=4)

    finished = datetime.now()
    print("* FINISHED @ %s took %s" % (datetime.now(), finished-started))
    

def parse_arguments():
    """Read arguments from commandline."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", metavar='logging verbosity', default=3, type=int, help='Verbosity of logging: 0-critical, 1-error, 2-warning, 3-info, 4-debug')
    parser.add_argument("-m", metavar='module to debug', help='Setting a module to debug automatically implies verbosity level debug')
    args = parser.parse_args()
    
    return args

# Application starts here
if __name__ == "__main__":
    args = parse_arguments()

    if args.m:
        # set module to debug (this will be the only loaded module)
        debug_module = args.m
    
        # set default logging to DEBUG if module given and logging verbosity not set
        args.v = 4    

    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING, 3: logging.INFO, 4: logging.DEBUG}
    logging.basicConfig(format='%(message)s', level=verbose[args.v], stream=sys.stdout)
    # logging.basicConfig(format='%(message)s', level=logging.INFO, stream=sys.stdout)

    main()
