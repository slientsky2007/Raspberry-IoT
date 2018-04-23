#!/usr/bin/env python3
import threading
import os
import sys
import time
import datetime
from OneNetAPI import onenet

try:
	import psutil
except ImportError:
	print("The psutil library was not found. Run 'sudo -H pip install psutil' to install it.")
	sys.exit()
  
class tcpu(threading.Thread):
	def __init__(self, timesleep):
		threading.Thread.__init__(self)
		self.cpum = ""
		self.cputimesleep = 1
		self.timesleep = timesleep
		
		self.onenet = onenet()
	
	def run(self):
		while True:
			time.sleep(self.cputimesleep)
			self.cpum = self.cpu_usage()

	def cpu_usage(self, interval=1):
		# load average, uptime
		uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
		cpu = psutil.cpu_percent(interval)
		self.onenet.num += 1
		if self.onenet.num >= 10:
			self.onenet.set("CPU", cpu)
			r = self.onenet.post()
			self.onenet.num = 0
		return "Cpu(s):%s Up:%s" \
			% (str(cpu)+'%', str(uptime).split('.')[0])	
		
		
