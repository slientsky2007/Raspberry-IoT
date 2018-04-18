#!/usr/bin/env python3
import fcntl
import struct
import datetime
import os
import sys
import time
import signal

#自定义类
from SYSTEMINFO import system
from CPUThread import cpu
from DHT22Thread import dht22
from BASICDEF import bytes2human
from SSD1306Thread import ssd1306

#轮子
import Adafruit_DHT
	
def main():
	#温湿度传感器DHT22
	sensor = Adafruit_DHT.DHT22
	#无线网卡在系统中的名称
	wlanname = "wlan0"
	#初始化网络流量对象
	netobj = nettest(wlanname)
	
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
	dht22thread = dht22(sensor, 24)
	#初始化OLED
	ssd1306thread = ssd1306()
	#因为cpu信息读取时导致阻塞比较奇怪，故抽取出来另起子线程，避免阻塞主线程
	cputhread = cpu(timesleep)
	#创建systeminfo对象，读取系统基础信息
	systeminfo = system(wlanname)

	#先初始化硬件设备，启动子线程
	dht22thread.start()
	cputhread.start()
	#默认第一次刷新屏幕，输出为空;	
	ssd1306thread.start()
	
	while True:
		#每次刷新数据间隔时间
		time.sleep(timesleep)
		
		#OLED子线程默认1秒刷新一次屏幕，
		#主线程不断循环提交需要显示的数据给OLED就ok了
		ssd1306thread.set_display(x, y, datem, cpum, memm, ipadd, netm, thm)
		
		#先判断子线程是否获取到数据，如果不为空则重新启动子线程
		#如果还没有获取到数据，则原子线程继续运行，等待获取读数
		if cputhread.cpum != "":
			#每次子线程执行完毕获取读数后，赋值给主线程对应变量
			#(PS:这样做是为了保持oled上一直有数据展示,但展示的数据不是实时的)
			cpum = cputhread.cpum
			cputhread = cpu(timesleep)
			cputhread.start()

		if dht22thread.thm != "":
			thm = dht22thread.thm
			dht22thread = dht22(sensor, 24)
			dht22thread.start()
		
		#自定义signal handler，如果执行的方法超时，则抛出异常继续循环
		#应该将系统基本信息获取方法抽取出来做成system类
		try:
			signal.signal(signal.SIGALRM, handler)
			signal.alarm(timesleep)
			
			datem = str(system.getDateTime())
			memm = system.get_mem_usage()
			ipadd = "Wlan0: " + system.getIP()
			netm = system.get_RT_network_traffic(timesleep)
			
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