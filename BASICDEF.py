#!/usr/bin/env python3

import sys, time, os

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