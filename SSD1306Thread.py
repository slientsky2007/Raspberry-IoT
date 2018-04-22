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

  
class tssd1306(threading.Thread):
	def __init__(self, timesleep=1):
		threading.Thread.__init__(self)
		self.timesleep = timesleep
		self.welcometimesleep = 5
		
		#串口设备i2c ssd1306 128*64 OLED 显示器
		self.serial = i2c(port=1, address=0x3C)
		self.oled = ssd1306(self.serial)
		self.cout = 10
		
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
		self.apm10 = ''
		self.apm25 = ''
		self.pm10 = ''
		self.pm25 = ''
		self.gt03um = ''
		self.gt05um = ''
		self.gt10um = ''
		self.gt25um = ''
	
	def run(self):
		try:
			while True:
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
				draw.text((x, y), self.thm, font=self.font2, fill="white")
				draw.text((x, y+10), self.apm25, font=self.font2, fill="white")
				draw.text((x, y+20), self.pm10, font=self.font2, fill="white")
				draw.text((x, y+30), self.pm25, font=self.font2, fill="white")
				draw.text((x, y+40), self.gt03um, font=self.font2, fill="white")
				draw.text((x, y+50), self.gt05um, font=self.font2, fill="white")
				
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
		self.cpum = cpum
		self.memm = memm
		self.ipadd = ipadd
		self.netm = netm
		
	def set_display_2(self, x, y, humidity, temperature, apm10, apm25, pm25, pm10, gt03um, gt05um, gt10um, gt25um):
		self.x = x
		self.y = y
		T = str(temperature) + '%'
		H = str(humidity) + u'°C'
		self.thm = "T&H: %s | %s" % \
				(T, H)
		self.apm10 = 'apm2.5: %sug/m^3'%(str(apm25))
		self.apm25 = 'apm2.5: %sug/m^3'%(str(apm25))
		self.pm10 = 'pm1.0: %sug/m^3'%(str(pm10))
		self.pm25 = 'pm2.5: %sug/m^3'%(str(pm25))
		self.gt03um = 'gt0.3um: %s/0.1L^3'%(str(gt03um))
		self.gt05um = 'gt0.5um: %s/0.1L^3'%(str(gt05um))
		self.gt10um = 'gt1.0um: %s/0.1L^3'%(str(gt10um))
		self.gt25um = 'gt2.5um: %s/0.1L^3'%(str(gt25um))

	#设置开屏信息
	def set_welcomemessage(self, welcomemessage):
		self.welcomemessage = welcomemessage
	
	#屏幕子线程中直接读取时间信息显示
	def getDateTime(self):
		dt = datetime.datetime.now()
		return dt.strftime( '%x %H:%M:%S %p' )
