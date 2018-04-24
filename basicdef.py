#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    basicdef
   Description :  常用方法
   Author :       Slientsky
   date：         2018-04-23
-------------------------------------------------
   Change Activity:
                   2018-04-23
-------------------------------------------------
"""

import time, os
import json, argparse, sys

class BasicDef():
	deviceid = None
	apikey = None
	
	def set_device_id(value):
		BasicDef.deviceid = value
	
	def set_apikey(value):
		BasicDef.apikey = value
	
	def get_device_id():
		return BasicDef.deviceid
	
	def get_apikey():
		return BasicDef.apikey
	
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

	def get_pares_info(argv, key, int=0):
		args = parse_args(argv[1:])
		# print('args: ', args)
		config = parse(args.configfile[int])
		print()
		info = config[args.device]
		value = info[key]
		return value
		
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

