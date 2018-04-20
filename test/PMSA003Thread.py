#!/usr/bin/env python3
import threading
import os
import sys
import time
import serial
import datetime
  
class pmsa003(threading.Thread):
	def __init__(self, timesleep=2):
		threading.Thread.__init__(self)
		self.pmdatas = ""
		self.timesleep = timesleep
		#usb口转UART
		self.pm_device = '/dev/ttyUSB0'
		self.open_pm_port()
		
		self.apm10 = ""
		self.apm25 = ""
		self.apm100 = ""
		self.pm25 = ""
		self.pm10 = ""
		self.pm100 = ""
		self.gt03um = ""
		self.gt05um = ""
		self.gt10um = ""
		self.gt25um = ""
		self.gt50um = ""
		self.gt100um = ""
		
		self.pm_res = False
	
	def run(self):
		while True:
			time.sleep(self.timesleep)
			self.pm_res = self.get_pm_data()
			if self.pm_res == False:
				continue

			self.apm10 = str(self.pm_res['apm10'])
			self.apm25 = str(self.pm_res['apm25'])
			self.apm100 = str(self.pm_res['apm100'])
			self.pm25 = str(self.pm_res['pm25'])
			self.pm10 = str(self.pm_res['pm10'])
			self.pm100 = str(self.pm_res['pm100'])
			self.gt03um = str(self.pm_res['gt03um'])
			self.gt05um = str(self.pm_res['gt05um'])
			self.gt10um = str(self.pm_res['gt10um'])
			self.gt25um = str(self.pm_res['gt25um'])
			self.gt50um = str(self.pm_res['gt50um'])
			self.gt100um = str(self.pm_res['gt100um'])
			
			
	def open_pm_port(self):
		self.port = serial.Serial(self.pm_device, baudrate=9600, timeout=2.0)
        #默认主动模式，不需要发送数据
		#self.port.write(b'\x42\x4D\xE1\x00\x00\x01\x70')
		
	def read_pm_line(self):
		rv = b''
		while True:
			ch1 = self.port.read()
			if ch1 == b'\x42':
				ch2 = self.port.read()
				if ch2 == b'\x4d':
					rv += ch1 + ch2
					rv += self.port.read(30)
					return rv
	
	def get_pm_data(self):
		#self.port.write(b'\x42\x4D\xE2\x00\x00\x01\x71')
		rcv = self.read_pm_line()
		# print(rcv)
		if sum(rcv[:-2]) == rcv[-2] * 256 + rcv[-1]:
			res = {'timestamp': datetime.datetime.now(),
					'apm10': rcv[4] * 256 + rcv[5],
					'apm25': rcv[6] * 256 + rcv[7],
					'apm100': rcv[8] * 256 + rcv[9],
					'pm10': rcv[10] * 256 + rcv[11],
					'pm25': rcv[12] * 256 + rcv[13],
					'pm100': rcv[14] * 256 + rcv[15],
					'gt03um': rcv[16] * 256 + rcv[17],
					'gt05um': rcv[18] * 256 + rcv[19],
					'gt10um': rcv[20] * 256 + rcv[21],
					'gt25um': rcv[22] * 256 + rcv[23],
					'gt50um': rcv[24] * 256 + rcv[25],
					'gt100um': rcv[26] * 256 + rcv[27]}
			return res
		else:
			return False
		
	#传感器XX数据校验，将偏差值较大数据丢弃
	def checkT():
		return ""
		
def main():
	pmsa003thread = pmsa003()
	pmsa003thread.start()
	
	while True:
		time.sleep(2)
		if pmsa003thread.pm_res == False:
			continue
			
		print("apm2.5: " + pmsa003thread.apm25 + "ug/m^3")
		print("apm1.0: " + pmsa003thread.apm10 + "ug/m^3")
		print("apm10: " + pmsa003thread.apm100 + "ug/m^3")
		print("pm2.5: " + pmsa003thread.pm25 + "ug/m^3")
		print("pm1.0: " + pmsa003thread.pm10 + "ug/m^3")
		print("pm10: " + pmsa003thread.pm100 + "ug/m^3")
		print("gt0.3um: " + pmsa003thread.gt03um + "n/0.1L^3")
		print("gt0.5um: " + pmsa003thread.gt05um + "n/0.1L^3")
		print("gt1.0um: " + pmsa003thread.gt10um + "n/0.1L^3")
		print("gt2.5um: " + pmsa003thread.gt25um + "n/0.1L^3")
		print("gt5.0um: " + pmsa003thread.gt50um + "n/0.1L^3")
		print("gt10um: " + pmsa003thread.gt100um + "n/0.1L^3")
		print("--------------------------------")
		

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass