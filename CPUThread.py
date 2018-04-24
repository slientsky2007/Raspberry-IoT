#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    CPUThread
   Description :  子线程，获取CPU信息
   Author :       Slientsky
   date：         2018-04-23
-------------------------------------------------
   Change Activity:
                   2018-04-23
-------------------------------------------------
"""

import threading
import os
import sys
import time
import datetime

from onenetapi import OneNetApi

try:
	import psutil
except ImportError:
	print("The psutil library was not found. Run 'sudo -H pip install psutil' to install it.")
	sys.exit()
  
class tcpu(threading.Thread):
	def __init__(self, timesleep, post2OneNet):
		threading.Thread.__init__(self)
		self.cpum = ""
		self.cputimesleep = 1
		self.timesleep = timesleep
		
		self.onenet = OneNetApi()
		self.post2OneNet = post2OneNet
	
	def run(self):
		while True:
			time.sleep(self.cputimesleep)
			self.cpum = self.cpu_usage()

	def cpu_usage(self, interval=1):
		# load average, uptime
		uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
		cpu = psutil.cpu_percent(interval)
		
		if self.post2OneNet:
			self.onenet.num += 1
			if self.onenet.num >= 10:
				self.onenet.set("CPU", cpu)
				r = self.onenet.post_data_flow()
				self.onenet.num = 0

		return "Cpu(s):%s Up:%s" \
			% (str(cpu)+'%', str(uptime).split('.')[0])	
		
		
