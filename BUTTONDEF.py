#!/usr/bin/env python3
import threading
import os
import sys
import time
import RPi.GPIO as GPIO

class tbutton(threading.Thread):
	def __init__(self, pin, oled):
		threading.Thread.__init__(self)
		self.oled = oled
		self.timesleep = 1
		self.pin = pin
		self.bt1_in_value = 0
		self.press_time = 1
		self.count_down = 10
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin,GPIO.IN)
		
		GPIO.add_event_detect(pin, GPIO.FALLING, callback= self.onPress,bouncetime=500)

	def onPress(self, channel):
		# print('pressed')
		self.press_time+=1
		if self.press_time >5:
			self.press_time=1
			self.oled.display = 0
		elif self.press_time==2:
			self.oled.display = 2
		elif self.press_time==3:
			print('python will close in %s'%(self.count_down))
			self.count_down=10
			self.oled.count = 10
			self.oled.display = 3
		elif self.press_time==4:
			print('system will restart in %s'%(self.count_down))
			self.count_down=10
			self.oled.count = 10
			self.oled.display = 4
		elif self.press_time==5:
			print('system will halt in %s'%(self.count_down))
			self.count_down=10
			self.oled.count = 10
			self.oled.display = 5
		

	def run(self):
		try:
			while True:
				if self.press_time==3 and self.oled.count <=0:
					self.oled.count = 10
					print("now close python app")
					
				elif self.press_time==4 and self.oled.count <=0:
					self.oled.count = 10
					print("now restart system")
					
				elif self.press_time==5 and self.oled.count <=0:
					self.oled.count = 10
					print("system now shutdown")
				
				# print(' '+ str(self.oled.count))	
				time.sleep(self.timesleep)
		except KeyboardInterrupt:
			raise
		finally:
			self.cleanup()
			
	def cleanup(self):
		'''释放资源，不然下次运行是可能会收到警告
		'''
		print('clean up')
		GPIO.cleanup()