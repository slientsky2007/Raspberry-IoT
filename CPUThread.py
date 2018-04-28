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
		self.__flag = threading.Event()     # 用于暂停线程的标识
		self.__flag.set()       # 设置为True
		self.__running = threading.Event()      # 用于停止线程的标识
		self.__running.set()      # 将running设置为True
		#setDaemon(True)当主线程结束之后，会杀死子线程;如果加上join,并设置等待时间，就会等待线程一段时间再退出
		self.setDaemon(True)
		self.cpum = ""
		self.cputimesleep = 1
		self.timesleep = timesleep
		
		self.onenet = OneNetApi()
		self.post2OneNet = post2OneNet
	
	def run(self):
		while self.__running.isSet():
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

		return [cpu, uptime]
		
	def pause(self):
		self.__flag.clear()     # 设置为False, 让线程阻塞

	def resume(self):
		self.__flag.set()    # 设置为True, 让线程停止阻塞

	def stop(self):
		self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
		self.__running.clear()        # 设置为False
