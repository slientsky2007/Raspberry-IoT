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
import threading
import os
import sys
import time
import serial
import datetime

#自定义类
from onenetapi import OneNetApi
from basicdef import BasicDef
  
class tpmsa003(threading.Thread):
	def __init__(self, usbdevice, post2OneNet, timesleep=2):
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
			
		self.timestamp = None
		self.apm10 = 0
		self.apm25 = 0
		self.apm100 = 0
		self.pm25 = 0
		self.pm10 = 0
		self.pm100 = 0
		self.gt03um = 0
		self.gt05um = 0
		self.gt10um = 0
		self.gt25um = 0
		self.gt50um = 0
		self.gt100um = 0
		self.all_PMS = []
		
		self.pm_res = False
		self.is_device = True
		
		self.post2OneNet = post2OneNet
		if post2OneNet:
			self.onenet = OneNetApi()
	
	def run(self):
		#初始化pm传感器失败时
		try:
			self.open_pm_port()
		except OSError as e:
			self.is_device = False
			print("Unable to connect to %s", self.device)
			return self.is_device
		while self.__running.isSet():
			time.sleep(self.timesleep)
			self.pm_res = self.get_pm_data()
			if self.pm_res == False:
				continue

			self.timestamp = self.pm_res['timestamp']
			self.apm10 = self.pm_res['apm10']
			self.apm25 = self.pm_res['apm25']
			self.apm100 = self.pm_res['apm100']
			self.pm25 = self.pm_res['pm25']
			self.pm10 = self.pm_res['pm10']
			self.pm100 = self.pm_res['pm100']
			self.gt03um = self.pm_res['gt03um']
			self.gt05um = self.pm_res['gt05um']
			self.gt10um = self.pm_res['gt10um']
			self.gt25um = self.pm_res['gt25um']
			self.gt50um = self.pm_res['gt50um']
			self.gt100um = self.pm_res['gt100um']
			self.all_PMS = [self.apm10, self.apm25, self.apm100, self.pm10, self.pm25, self.pm100, self.gt03um, self.gt05um, self.gt10um, self.gt25um, self.gt50um, self.gt100um]
			
			if self.post2OneNet:
				self.onenet.num += 1
				if self.onenet.num >= 10:
					if BasicDef.get_network_status():
						self.onenet.set_post_data_flow("apm10", self.apm10)
						self.onenet.set_post_data_flow("apm25", self.apm25)
						self.onenet.set_post_data_flow("pm10", self.pm10)
						self.onenet.set_post_data_flow("pm25", self.pm25)
						# self.onenet.set_post_data_flow("gt03um", self.gt03um)
						# self.onenet.set_post_data_flow("gt05um", self.gt05um)
						r = self.onenet.post_data_flow()
					self.onenet.num = 0
					
	def open_pm_port(self):
		self.port = serial.Serial(self.device, baudrate=9600, timeout=2.0)
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
		rcv = self.read_pm_line()
		# print(rcv)
		if sum(rcv[:-2]) == rcv[-2] * 256 + rcv[-1]:
			res = {'timestamp': self.getDateTime(),
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
	
	def getDateTime(self):
		dt = datetime.datetime.now()
		return dt.strftime( '%x %H:%M:%S %p' )
		
	def pause(self):
		self.__flag.clear()     # 设置为False, 让线程阻塞

	def resume(self):
		self.__flag.set()    # 设置为True, 让线程停止阻塞

	def stop(self):
		self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
		self.__running.clear()        # 设置为False