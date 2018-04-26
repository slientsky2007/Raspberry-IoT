#!/usr/bin/env python3
import threading
import os
import sys
import time
import RPi.GPIO as GPIO

class button(threading.Thread):
	def __init__(self, pin):
		threading.Thread.__init__(self)
		self.timesleep = 1
		self.pin = pin
		self.bt1_in_value = 0
		self.press_time = 0
		self.count_down = 10
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin,GPIO.IN)
		
		GPIO.add_event_detect(pin, GPIO.FALLING, callback= self.onPress,bouncetime=500)

	def onPress(self, channel):
		# print('pressed')
		self.press_time+=1
		if self.press_time >3:
			self.press_time=1
		if self.press_time==1:
			self.count_down=10
			print('system will restart in %s'%(self.count_down))
		elif self.press_time==2:
			self.count_down=10
			print('system will halt in %s'%(self.count_down))
		elif self.press_time==3:
			print ('cancel')
			self.count_down=10

	def run(self):
		try:
			while True:
				if self.count_down <= 0:
					self.count_down = 10
					
				if self.press_time==1:
					self.count_down -= 1
					print(' '+ str(self.count_down))
					
				elif self.press_time==2:
					self.count_down -= 1
					print(' '+ str(self.count_down))
					
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

def main():
	bt1 = button(23)
	bt1.start()	
	
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass