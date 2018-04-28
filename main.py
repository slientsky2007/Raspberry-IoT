#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    main
   Description :  主线程启动
   Author :       Slientsky
   date：         2018-04-23
-------------------------------------------------
   Change Activity:
                   2018-04-23
-------------------------------------------------
"""
import sys, os
import time
import signal

#自定义类
from CPUThread import tcpu
from Button import button
from DHT22Thread import tdht22
from SSD1306Thread import tssd1306
from PMSA003Thread import tpmsa003

from systeminfo import SystemInfo
from basicdef import BasicDef

def main(argv):
	#休眠时间/秒
	timesleep = 1
	button_GPIO = 23
	dht22_GPIO = 24
	pmsa003_USB = '/dev/ttyUSB0'
	#无线网卡名称
	wlan_name = "wlan0"
	
	system_shutdown = False
	#是否上传数据到OneNet平台
	post2OneNet = False
	#检查参数是否存在
	if argv[1:] == []:
		print("Parameters Not exsit! Data won't post to OnetNet")
	#检查配置文件是否存在;
	elif (os.path.isfile(argv[1]) == False):
		print("file: "+ argv[1] + " not exist! Data won't post to OneNet")
	else:
		#检查配置文件中参数是否正确
		try:
			_deviceid = basic.get_pares_info(argv, 'deviceid')
			# print('_deviceid: ', _deviceid)
			_apikey = basic.get_pares_info(argv, 'apikey')
			# print('_apikey: ', _apikey)
			BasicDef.set_device_id(_deviceid)
			BasicDef.set_apikey(_apikey)
			
			post2OneNet = True
		except KeyError as e:
			print("--device=%s is not exsit! Data won't post to OneNet" % e)
	
	#初始化要OLED显示的内容
	cpum = ""
	datem = ""
	memm = ""
	ipadd = ""
	netm = ""

	#初始化传感器和子线程
	#传感器设备数据读取存在延时，新起子线程异步执行，避免阻塞主线程
	dht22thread = tdht22(dht22_GPIO)
	#初始化Pm传感器，为了读数准确，传感器需要预热30秒时间
	pmsa003thread = tpmsa003(pmsa003_USB)

	#初始化OLED
	ssd1306thread = tssd1306()
	#因为cpu信息读取时导致阻塞比较奇怪，故抽取出来另起子线程，避免阻塞主线程
	cputhread = tcpu(timesleep, post2OneNet)
	#创建systeminfo对象，读取系统基础信息
	systeminfo = SystemInfo(wlan_name, post2OneNet)

	#按键操作
	button_1 = button(button_GPIO, ssd1306thread)
	
	#先初始化硬件设备，启动子线程
	cputhread.start()
	ssd1306thread.start()
	#传感器子线程后面启动，因为：
	pmsa003thread.start()
	dht22thread.start()

	
	while True:
		#每次刷新数据时间间隔
		time.sleep(timesleep)
		
		#默认显示欢迎界面，OLED子线程默认1秒刷新一次屏幕;
		
		#自定义signal handler，如果执行的方法超时，则抛出异常继续循环
		#应该将系统基本信息获取方法抽取出来做成system类
		try:
			signal.signal(signal.SIGALRM, handler)
			signal.alarm(timesleep)
			
			#系统基础信息
			#(由于使用子线程异步读取数据，故存在时间差，
			#为了时间显示比较正常，将时间获取放在绘制屏幕子线程中执行)
			# datem = str(systeminfo.getDateTime())			
			memm = systeminfo.get_mem_usage()
			ipadd = systeminfo.getIP()
			netm = systeminfo.get_RT_network_traffic(timesleep)
			
			#子线程自身不断循环获取最新读数
			cpum = cputhread.cpum

			#由于传感器子线程默认timesleep=1并且需要等待读取数据，传感器读取的值是异步的，会有延时	
			#主线程不断循环设置需要显示的数据给OLED子线程就ok了;
			if ssd1306thread.display == 1:
				ssd1306thread.set_display_1(0, 10, cpum, memm, ipadd, netm)
			elif ssd1306thread.display == 2:
				ssd1306thread.set_display_2(0, 0, dht22thread.H, dht22thread.T, pmsa003thread.apm10, pmsa003thread.apm25, pmsa003thread.apm100, pmsa003thread.pm10, pmsa003thread.pm25, pmsa003thread.pm100, pmsa003thread.gt03um, pmsa003thread.gt05um, pmsa003thread.gt10um, pmsa003thread.gt25um, pmsa003thread.gt50um, pmsa003thread.gt100um)
			elif ssd1306thread.display == 3 and ssd1306thread.count <= 0:
				# """Restarts the current program. 
				# Note: this function does not return. Any cleanup action (like 
				# saving data) must be done before calling this function."""  
				# python = sys.executable  
				# os.execl(python, python, * sys.argv)
				print("Programe off")
				ssd1306thread.stop()
				cputhread.stop()
				pmsa003thread.stop()
				dht22thread.stop()
				time.sleep(3)
				sys.exit(0)
				
			elif ssd1306thread.display == 4 and ssd1306thread.count <= 0:
				system_reboot = True
				print("system rebooting")
				ssd1306thread.stop()
				cputhread.stop()
				pmsa003thread.stop()
				dht22thread.stop()
				time.sleep(3)
				break
				
			elif ssd1306thread.display == 5 and ssd1306thread.count <= 0:
				system_shutdown = True
				print("system off")
				ssd1306thread.stop()
				cputhread.stop()
				pmsa003thread.stop()
				dht22thread.stop()
				time.sleep(3)
				break
			
			signal.alarm(0)
			
		except AssertionError:
			continue
		
	if system_reboot: os.system('sudo reboot')
	elif system_shutdown: os.system('sudo halt')
		
if __name__ == "__main__":
	def handler(signum, frame):
		raise AssertionError
		
	try:
		main(sys.argv)
	except KeyboardInterrupt:
		sys.exit(0)