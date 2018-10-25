# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol vergrabber@kingu.pl
"""
Helper library to process actual software versions of different kinds provided by modules
"""
import glob
import importlib
from datetime import datetime, timedelta, date
	
modules = []
editions = []

# def getStableEditions(product):
	# """ Return latest stable editions of given software
	
	# :param software: name of the software
	# :return: Latest stable editions of given software
	# :rtype: [Softver]
	# """
	# result = []
	# for edition in editions:
		# if edition.product == product and edition.stable:
			# result.append(edition)
	
	# return(result)	

# def getLatestEdition(product):
	# """ Return latest edition & version of given software
	
	# :param software: name of the software
	# :return: Latest edition of given software
	# :rtype: Softver
	# """
	# #for mod in modules:
		# # if(mod["outdated"])
	# for edition in editions:
		# if edition.product == product and edition.latest:
			# return edition
	
	# return(None)	


def addEdition(item):
	"""	Appends product edition to list of product editions
	"""
	if(type(item) is Softver):
		editions.append(item)
	else:
		raise Exception("Invalid type: cannot add ", type(item), " to editions list, Softver type expected")


def loadModules(folder = 'servers', name = None):
	"""	Loads modules (plugins) required for grabbing software editions and versions
	"""
	del modules[:]
	del editions[:]
	pattern = '[!_]*' if name == None else name
	for filename in glob.iglob(folder+'/'+ pattern +'.py'):
		name = filename.replace(".py","").replace("/",".")
		modules.append(importlib.import_module(name))
	return modules
		
		
class Softver:
	def __init__(self, product="unknown", edition=None, version="0.0.0", 
				stable = False, latest = False, 
				released = date.max, ends = date.min,
				lts = None):
		self.product = product
		self.edition = edition
		self.version = version
		self.stable = stable
		self.latest = latest
		self.released = released
		self.ends = ends
		self.lts = lts
	
	