#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    DHT22Thread
   Description :  子线程，获取温湿度传感器数据
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

#自定义类
from onenetapi import OneNetApi
from basicdef import BasicDef

#轮子
import Adafruit_DHT

class tdht22(threading.Thread):
	def __init__(self, pin, post2OneNet):
		threading.Thread.__init__(self)
		self.__flag = threading.Event()     # 用于暂停线程的标识
		self.__flag.set()       # 设置为True
		self.__running = threading.Event()      # 用于停止线程的标识
		self.__running.set()      # 将running设置为True
		#setDaemon(True)当主线程结束之后，会杀死子线程;如果加上join,并设置等待时间，就会等待线程一段时间再退出
		self.setDaemon(True)
		self.T_H = [0, 0]
		self.timesleep = 1
		#温湿度传感器DHT22
		self.sensor = Adafruit_DHT.DHT22
		self.pin = pin
		
		self.onenet = OneNetApi()
		self.post2OneNet = post2OneNet
	
	def run(self):
		while self.__running.isSet():
			time.sleep(self.timesleep)
			is_T_H = self.getTH()
			if is_T_H != False:
				self.T_H = is_T_H
				if self.post2OneNet:
					self.onenet.num += 1
					if self.onenet.num >= 10:
						if BasicDef.get_network_status():
							self.onenet.set("T", self.T_H[0])
							self.onenet.set("H", self.T_H[1])
							r = self.onenet.post_data_flow()
						self.onenet.num = 0

	def getTH(self):
		try:
			humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)#24 是 GPIO 的引脚编号
			# print(humidity, end='')
			# print("   ", end='')
			# print(temperature)
		except OSError as e:
			print("Can't find DHT22")
			return False
		
		if humidity == None:
			return False
		if temperature == None:
			return False

		H = round(humidity,2)
		T = round(temperature,2)

		return [T, H]

	#传感器温度数据校验，将偏差值较大数据丢弃
	def checkT():
		return ""
	#传感器湿度数据校验，将偏差值较大数据丢弃
	def checkH():
		return ""

	def pause(self):
		self.__flag.clear()     # 设置为False, 让线程阻塞

	def resume(self):
		self.__flag.set()    # 设置为True, 让线程停止阻塞

	def stop(self):
		self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
		self.__running.clear()        # 设置为False
		
