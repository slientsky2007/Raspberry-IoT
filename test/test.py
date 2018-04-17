#!/usr/bin/env python3 
import sys, time, os
from net import nettest

def main():  
	timesleep = 1
	netobj = nettest("wlan0")
	while True:
		time.sleep(timesleep)
		print(netobj.network(timesleep))

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass
