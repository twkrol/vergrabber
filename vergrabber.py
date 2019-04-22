# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol vergrabber@kingu.pl
"""
Helper library to process actual software versions of different kinds provided by modules
"""
import glob
import importlib.util
from datetime import datetime, timedelta, date
from pathlib import Path
	
modules = []
editions = []


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
	data_folder = Path(folder)

	for filename in data_folder.glob(pattern + ".py"):
		module = importlib.import_module(folder + "." + filename.stem)
		modules.append(module)

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
	
	