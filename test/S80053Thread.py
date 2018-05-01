#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    PMSA003Thread
   Description :  子线程，获取pm传感器数据
   Author :       Slientsky
   date：         2018-04-23
-------------------------------------------------
   Change Activity:
                   2018-04-23
-------------------------------------------------
"""
import time
import threading
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.diag_message import *
from pymodbus.file_message import *
from pymodbus.other_message import *
from pymodbus.mei_message import *

#自定义类
from onenetapi import OneNetApi
  
class ts80053(threading.Thread):
	def __init__(self, usbdevice, post2OneNet=False, timesleep=2):
		threading.Thread.__init__(self)
		self.__flag = threading.Event()     # 用于暂停线程的标识
		self.__flag.set()       # 设置为True
		self.__running = threading.Event()      # 用于停止线程的标识
		self.__running.set()      # 将running设置为True
		#setDaemon(True)当主线程结束之后，会杀死子线程;如果加上join,并设置等待时间，就会等待线程一段时间再退出
		self.setDaemon(True)
		
		self.timesleep = timesleep
		#usb口转UART CH340
		self.device = usbdevice
		self.client = None
		
		self.is_device = True
		
		self.post2OneNet = post2OneNet
		if post2OneNet:
			self.onenet = OneNetApi()
	
	def run(self):
		while self.__running.isSet():
			time.sleep(self.timesleep)
			if self.connect_s80053():
				self.co2 = self.read_CO2()
	
	def connect_s80053(self):
		self.client = ModbusSerialClient(method='rtu', port=self.device, stopbits=1, bytesize=8, baudrate=9600, timeout=0.5)
		if not self.client.connect():
			self.is_device = False
			print("Unable to connect to %s", self.device)
			return False
		else:
			return True
			
	def close(self):
		self.client.close()
		
	def read_CO2(self):
		response = self.client.read_input_registers(address=3, count=1, unit=0xFE )
		co2 = response.getRegister(0)
		return co2
		
	#传感器XX数据校验，将偏差值较大数据丢弃
	def check():
		return ""
		
	def pause(self):
		self.__flag.clear()     # 设置为False, 让线程阻塞

	def resume(self):
		self.__flag.set()    # 设置为True, 让线程停止阻塞

	def stop(self):
		self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
		self.__running.clear()        # 设置为False
		self.close()

def main():
	usbdevice = '/dev/ttyUSB0'
	s80053thread = ts80053(usbdevice)
	
	if not s80053thread.connect_s80053():
		sys.exit(0)
	else:
		s80053thread.start()
	while True:
		time.sleep(3)
		print(s80053thread.co2)
			

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass