#!/usr/bin/env python3
import threading
import os
import sys
import time

#轮子
import Adafruit_DHT

  
class dht22(threading.Thread):
	def __init__(self, sensor, pin):
		threading.Thread.__init__(self)
		self.thm = ""
		self.timesleep = 1
		self.sensor = sensor
		self.pin = pin
	
	def run(self):
		while True:
			time.sleep(self.timesleep)
			self.thm = self.getTH(self.sensor, self.pin)

	def getTH(self, sensor, pin):
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)#24 是 GPIO 的引脚编号
		H = str(round(humidity,2)) + '%'
		a = u'°C'
		T = str(round(temperature,2)) + a
		return "T&H:%s|%s" % \
				(T, H)	
	
	#传感器温度数据校验，将偏差值较大数据丢弃
	def checkT():
		return ""
	#传感器湿度数据校验，将偏差值较大数据丢弃
	def checkH():
		return ""
		
