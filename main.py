#!/usr/bin/env python3
# import datetime
# import os
# import sys
import time
import signal

#自定义类
from SYSTEMINFO import system
from CPUThread import tcpu
from DHT22Thread import tdht22
from SSD1306Thread import tssd1306
	
def main():

	#无线网卡在系统中的名称
	wlanname = "wlan0"
	
	#休眠时间/秒
	timesleep = 1
	
	#初始化要OLED显示的内容
	x = 0
	y = 0
	cpum = ""
	thm = ""
	datem = ""
	memm = ""
	ipadd = ""
	netm = ""

	#初始化传感器和子线程
	#传感器设备数据读取存在延时，新起子线程异步执行，避免阻塞主线程
	dht22thread = tdht22(24)
	#初始化OLED
	ssd1306thread = tssd1306()
	#因为cpu信息读取时导致阻塞比较奇怪，故抽取出来另起子线程，避免阻塞主线程
	cputhread = tcpu(timesleep)
	#创建systeminfo对象，读取系统基础信息
	systeminfo = system(wlanname)

	#先初始化硬件设备，启动子线程
	dht22thread.start()
	cputhread.start()
	ssd1306thread.start()
	
	while True:
		#每次刷新数据间隔时间
		time.sleep(timesleep)
		
		#默认显示欢迎界面，OLED子线程默认1秒刷新一次屏幕;
		#主线程不断循环设置需要显示的数据给OLED子线程就ok了;
		ssd1306thread.set_display(x, y, datem, cpum, memm, ipadd, netm, thm)
		
		#自定义signal handler，如果执行的方法超时，则抛出异常继续循环
		#应该将系统基本信息获取方法抽取出来做成system类
		try:
			signal.signal(signal.SIGALRM, handler)
			signal.alarm(timesleep)
			
			#系统基础信息
			datem = str(systeminfo.getDateTime())
			memm = systeminfo.get_mem_usage()
			ipadd = "Wlan0: " + systeminfo.getIP()
			netm = systeminfo.get_RT_network_traffic(timesleep)
			
			#子线程自身不断循环获取最新读数
			#由于传感器子线程默认timesleep=1并且需要等待读取数据，传感器读取的值是异步的，会有延时
			thm = dht22thread.thm
			cpum = cputhread.cpum
			
			signal.alarm(0)
			
		except AssertionError:
			continue

if __name__ == "__main__":
	def handler(signum, frame):
		raise AssertionError
		
	try:
		main()
	except KeyboardInterrupt:
		pass