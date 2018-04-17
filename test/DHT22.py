#!/usr/bin/env python3  

import Adafruit_DHT

def getTH(device):
	humidity, temperature = Adafruit_DHT.read_retry(device, 24)#24 是 GPIO 的引脚编号
	H = str(round(humidity,2)) + '%'
	a = u'°C'
	T = str(round(temperature,2)) + a
	return "T: %s, H: %s" % \
			(T, H)

def main():  
	sensor = Adafruit_DHT.DHT22
	
	while True:
		print(getTH(sensor))

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass