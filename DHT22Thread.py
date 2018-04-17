import threading
import os
import sys
import time
import Adafruit_DHT

try:
	import psutil
except ImportError:
	print("The psutil library was not found. Run 'sudo -H pip install psutil' to install it.")
	sys.exit()
  
class dht22(threading.Thread):
	def __init__(self, sensor, pin):
		threading.Thread.__init__(self)
		self.thm = ""
		self.sensor = sensor
		self.pin = pin
	
	def run(self):
		self.thm = self.getTH(self.sensor, self.pin)

	def getTH(self, sensor, pin):
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)#24 是 GPIO 的引脚编号
		H = str(round(humidity,2)) + '%'
		a = u'°C'
		T = str(round(temperature,2)) + a
		return "T&H:%s|%s" % \
				(T, H)	
		
		
