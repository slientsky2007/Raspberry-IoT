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
	serial = i2c(port=1, address=0x3C)
	sensor = Adafruit_DHT.DHT22
	oled = ssd1306(serial)
	timesleep = 1
	wlanname = "wlan0"
	netobj = nettest(wlanname)
    #font = ImageFont.load_default()  
    #@font2 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 14) 
	font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
								'fonts', 'C&C Red Alert [INET].ttf'))
	font2 = ImageFont.truetype(font_path, 12)
	
	cputhread = cpu(timesleep)
	cputhread.start()
	
	dht22thread = dht22(sensor, 24)
	dht22thread.start()
	
	cpum = ""
	thm = ""
	datem = ""
	memm = ""
	ipadd = ""
	netm = ""
	
	while True:
		
		if cputhread.cpum != "":
			cpum = cputhread.cpum
			cputhread = cpu(timesleep)
			cputhread.start()

		if dht22thread.thm != "":
			thm = dht22thread.thm
			dht22thread = dht22(sensor, 24)
			dht22thread.start()
		
		#等待子线程完成数据读取
		time.sleep(timesleep)
				
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

		stats(oled, font2, datem, cpum, memm, ipadd, netm, thm)


if __name__ == "__main__":
	def handler(signum, frame):
		raise AssertionError
		
	try:
		main()
	except KeyboardInterrupt:
		pass