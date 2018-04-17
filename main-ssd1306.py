#!/usr/bin/env python3  
  
from luma.core.interface.serial import i2c, spi  
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106  
from luma.core.render import canvas  
from PIL import ImageDraw, ImageFont  
  
import socket  
import fcntl  
import struct  
#from subprocess import Popen,PIPE

from  datetime  import  *
import os
import sys
import time

from net import nettest
from CPUThread import cpu
from DHT22Thread import dht22

import Adafruit_DHT

import signal

try:
	import psutil
except ImportError:
	print("The psutil library was not found. Run 'sudo -H pip install psutil' to install it.")
	sys.exit()

def bytes2human(n):
	"""
	>>> bytes2human(10000)
	'9K'
	>>> bytes2human(100001221)
	'95M'
	"""
	symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
	prefix = {}
	for i, s in enumerate(symbols):
		prefix[s] = 1 << (i + 1) * 10
	for s in reversed(symbols):
		if n >= prefix[s]:
			value = int(float(n) / prefix[s])
			return '%s%s' % (value, s)
	return "%sB" % n

def mem_usage():
	usage = psutil.virtual_memory()
	return "Mem: %s %.0f%% %s free" \
		% (bytes2human(usage.total), usage.percent, bytes2human(usage.free))
				
def getDate():
	dt = datetime.now()
	return dt.strftime( '%Y-%m-%d' )

def getTime():
	dt = datetime.now()
	return dt.strftime( '%H:%M:%S %p' )

def getDateTime():
	dt = datetime.now()
	return dt.strftime( '%x %H:%M:%S %p' )

  
def getIP(ifname):  
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   
    return socket.inet_ntoa(fcntl.ioctl(   
        s.fileno(),   
        0x8915,  # SIOCGIFADDR   
        struct.pack('256s', ifname[:15].encode('utf-8'))   
    )[20:24])  

def stats(oled, font2, datem, cpum, memm, ipadd, netm, thm):  

	with canvas(oled) as draw:
		draw.text((0, 0), datem, fill="white")
		draw.text((0, 10), cpum, font=font2, fill="white")
		draw.text((0, 20), memm, font=font2, fill="white")
		draw.text((0, 30), ipadd, font=font2, fill="white")
		draw.text((0, 40), netm, font=font2, fill="white")
		draw.text((0, 50), thm, font=font2, fill="white")
	
def main():
	#串口设备i2c ssd1306 128*64 OLED 显示器
	serial = i2c(port=1, address=0x3C)
	oled = ssd1306(serial)
	#温湿度传感器DHT22
	sensor = Adafruit_DHT.DHT22
	netobj = nettest(wlanname)
	wlanname = "wlan0"
	
	timesleep = 1

    #font = ImageFont.load_default() 
	font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
								'fonts', 'C&C Red Alert [INET].ttf'))
	font2 = ImageFont.truetype(font_path, 12)

	#因为cpu信息读取时导致阻塞比较奇怪，故另起子线程
	cputhread = cpu(timesleep)
	cputhread.start()
	#初始化传感器子线程
	#硬件设备数据读取存在延时，新起子线程异步执行，避免阻塞主线程
	dht22thread = dht22(sensor, 24)
	dht22thread.start()
	
	#初始化要OLED显示的内容
	cpum = ""
	thm = ""
	datem = ""
	memm = ""
	ipadd = ""
	netm = ""
	
	while True:
		#默认第一次刷新屏幕，输出为空;
		stats(oled, font2, datem, cpum, memm, ipadd, netm, thm)
		#每次刷新屏幕间隔时间
		time.sleep(timesleep)
		
		#先判断子线程是否获取到数据，如果不为空则重新启动子线程
		#如果还没有获取到数据，则原子线程继续运行，等待获取读数
		if cputhread.cpum != "":
			#每次子线程执行完毕获取读数后，赋值给主线程对应变量
			#(PS:这样做是为了保持oled上一直有数据展示,但展示的数据有可能不是实时的)
			cpum = cputhread.cpum
			cputhread = cpu(timesleep)
			cputhread.start()

		if dht22thread.thm != "":
			thm = dht22thread.thm
			dht22thread = dht22(sensor, 24)
			dht22thread.start()
				
		try:
			signal.signal(signal.SIGALRM, handler)
			signal.alarm(timesleep)
			
			datem = str(getDateTime())
			memm = mem_usage()
			ipadd = "Wlan0: " + getIP(wlanname)
			netm = netobj.network(timesleep)
			
			signal.alarm(0)
		except AssertionError:
			datem = ""
			memm = ""
			ipadd = ""
			netm = ""

if __name__ == "__main__":
	def handler(signum, frame):
		raise AssertionError
		
	try:
		main()
	except KeyboardInterrupt:
		pass