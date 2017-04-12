#!/usr/bin/env python2.7

import ConfigParser
import io

class ini(object):
	
	"""
	init config file object
	"""
	def __init__(self, cfg_file = "config.ini"):
		with open(cfg_file) as f:
			sample_config = f.read()
			self.config = ConfigParser.RawConfigParser(allow_no_value=True)
			self.config.readfp(io.BytesIO(sample_config))
			
	"""
	get content
	"""
	def get_data(self, section, key):
		try:
			return self.config.get(section, key)
		except:
			return ""
    