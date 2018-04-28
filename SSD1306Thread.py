#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    SSD1306Thread
   Description :  子线程，控制屏幕显示
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

#轮子
from luma.core.interface.serial import i2c, spi
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from luma.core.render import canvas
from PIL import ImageDraw, ImageFont

from basicdef import BasicDef

  
class tssd1306(threading.Thread):
	def __init__(self, timesleep=1):
		threading.Thread.__init__(self)
		self.__flag = threading.Event()     # 用于暂停线程的标识
		self.__flag.set()       # 设置为True
		self.__running = threading.Event()      # 用于停止线程的标识
		self.__running.set()      # 将running设置为True
		#setDaemon(True)当主线程结束之后，会杀死子线程;如果加上join,并设置等待时间，就会等待线程一段时间再退出
		self.setDaemon(True)
		
		self.timesleep = timesleep
		self.welcometimesleep = 5
		
		#串口设备i2c ssd1306 128*64 OLED 显示器
		self.serial = i2c(port=1, address=0x3C)
		self.oled = ssd1306(self.serial)
		self.count = 10
		
		#字体
		#font = ImageFont.load_default() 
		self.font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
								'fonts', 'C&C Red Alert [INET].ttf'))
		self.font2 = ImageFont.truetype(self.font_path, 12)
		
		#显示数据初始化
		self.x = 0
		self.y = 0
		#控制屏幕显示：0为欢迎界面 1为系统信息 2为传感器信息 3为关闭python进程 4为重启 5为关机
		self.display = 0
		self.datem = ""
		self.cpum = ""
		self.memm = ""
		self.ipadd = ""
		self.netm = ""
		self.welcomemessage = "Hi SlientSky"
		
		self.thm = ''
		self.co2 = ''
		self.apm10 = ''
		self.apm25 = ''
		self.apm100 = ''
		self.pm10 = ''
		self.pm25 = ''
		self.pm100 = ''
		self.gt03um = ''
		self.gt05um = ''
		self.gt10um = ''
		self.gt25um = ''
		
		self.aqi1 = ''
		self.aqi2 = ''
		self.aqi3 = ''
	
	def run(self):
		try:
			while self.__running.isSet():
				self.__flag.wait()
				self.stats()
				time.sleep(self.timesleep)
		except KeyboardInterrupt:
			raise

	def special_stats(self, x, y, message):
		with canvas(self.oled) as draw:
			if self.welcomemessage == "":
				draw.text((x, y), message, fill="white")
			
	def stats(self):
		x = self.x
		y = self.y
		with canvas(self.oled) as draw:
			if self.display == 0:
				draw.text((30, 25), self.welcomemessage, fill="white")
				time.sleep(self.welcometimesleep)
				self.display = 1
				
			elif self.display == 1:
				draw.text((x, y), self.getDateTime(), fill="white")
				draw.text((x, y+10), self.cpum, font=self.font2, fill="white")
				draw.text((x, y+20), self.memm, font=self.font2, fill="white")
				draw.text((x, y+30), self.ipadd, font=self.font2, fill="white")
				draw.text((x, y+40), self.netm, font=self.font2, fill="white")
				
			elif self.display == 2:
				draw.text((x, y+5), self.thm, font=self.font2, fill="white")
				draw.text((x, y+15), "CO2: ", font=self.font2, fill="white")
				draw.text((x, y+25), " APM | PM | Gtum", fill="white")
				draw.text((x, y+35), self.aqi1, font=self.font2, fill="white")
				draw.text((x, y+45), self.aqi2, font=self.font2, fill="white")
				draw.text((x, y+55), self.aqi3, font=self.font2, fill="white")
				
			elif self.display == 3:
				self.count -=1
				message = "python will close: " + str(self.count)
				draw.text((10, 25), message, font=self.font2, fill="white")
			elif self.display == 4:
				self.count -=1
				message = "system will restart in: " + str(self.count)
				draw.text((10, 25), message, font=self.font2, fill="white")
			elif self.display == 5:
				self.count -=1
				message = "system will halt in: " + str(self.count)
				draw.text((10, 25), message, font=self.font2, fill="white")				
	
	def set_display_1(self, x, y, cpum, memm, ipadd, netm):
		self.x = x
		self.y = y
		self.cpum = "Cpu(s):%s Up:%s" \
			% (str(cpum[0])+'%', str(cpum[1]).split('.')[0])
		self.memm = "Mem: %s %.0f%% %s free" \
			% (BasicDef.bytes2human(memm[0]), memm[1], BasicDef.bytes2human(memm[2]))
		self.ipadd = "Wlan0: " + ipadd
		self.netm = "Tx %s,  Rx %s" % \
				(netm[0], netm[1])
		
	def set_display_2(self, x, y, humidity, temperature, apm10, apm25, apm100, pm10, pm25, pm100, gt03um, gt05um, gt10um, gt25um, gt50um, gt100um):
		self.x = x
		self.y = y
		T = str(temperature) + '%'
		H = str(humidity) + u'°C'
		self.thm = "T&H: %s | %s" % \
				(T, H)
				
		self.aqi1 = '  %s   |  %s  |  %s'%(str(apm10), str(pm10), str(gt03um))
		self.aqi2 = '  %s   |  %s  |  %s'%(str(apm25), str(pm25), str(gt05um))
		self.aqi3 = '  %s   |  %s  |  %s'%(str(apm100), str(pm100), str(gt10um))
		# self.apm10 = 'apm1.0: %sug/m^3'%(str(apm10))
		# self.apm25 = 'apm2.5: %sug/m^3'%(str(apm25))
		# self.apm100 = 'apm10: %sug/m^3'%(str(apm100))		
		# self.pm10 = 'pm1.0: %sug/m^3'%(str(pm10))
		# self.pm25 = 'pm2.5: %sug/m^3'%(str(pm25))
		# self.pm100 = 'pm10: %sug/m^3'%(str(pm100))
		# self.gt03um = 'gt0.3um: %s/0.1L^3'%(str(gt03um))
		# self.gt05um = 'gt0.5um: %s/0.1L^3'%(str(gt05um))
		# self.gt10um = 'gt1.0um: %s/0.1L^3'%(str(gt10um))
		# self.gt25um = 'gt2.5um: %s/0.1L^3'%(str(gt25um))
		# self.gt50um = 'gt5.0um: %s/0.1L^3'%(str(gt50um))
		# self.gt100um = 'gt10um: %s/0.1L^3'%(str(gt100um))

	#设置开屏信息
	def set_welcomemessage(self, welcomemessage):
		self.welcomemessage = welcomemessage
	
	#屏幕子线程中直接读取时间信息显示
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