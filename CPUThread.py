import threading
import os
import sys
import time
import datetime

try:
	import psutil
except ImportError:
	print("The psutil library was not found. Run 'sudo -H pip install psutil' to install it.")
	sys.exit()
  
class cpu(threading.Thread):
	def __init__(self, timesleep):
		threading.Thread.__init__(self)
		self.cpum = ""
		self.timesleep = timesleep
	
	def run(self):
		self.cpum = self.cpu_usage()

	def cpu_usage(self, interval=1):
		# load average, uptime
		uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
		cpu = str(psutil.cpu_percent(interval))+"%"
		return "Cpu(s):%s Up:%s" \
			% (cpu, str(uptime).split('.')[0])	
		
		
