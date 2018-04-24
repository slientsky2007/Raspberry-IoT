#!/usr/bin/env python3

import time, os
import json, argparse, sys

class basic():

	@staticmethod
	def bytes2human(n):
		"""
		>>> bytes2human(10000)
		'9K'
		>>> bytes2human(100001221)
		'95M'
		"""
		symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
		prefix = {}
		for i, s in enumerate(symbols):
			prefix[s] = 1 << (i + 1) * 10
		for s in reversed(symbols):
			if n >= prefix[s]:
				value = int(float(n) / prefix[s])
				return '%s%s' % (value, s)
		return "%sB" % n

	def parse_args(args):  
		parser = argparse.ArgumentParser(prog="OneNetServer")  
		parser.add_argument('configfile', nargs=1, type=str, help='')  
		parser.add_argument('--device', default="device", type=str, help='')  
		return parser.parse_args(args)  
  
	def parse(filename):  
		configfile = open(filename)  
		jsonconfig = json.load(configfile)  
		configfile.close()  
		return jsonconfig 