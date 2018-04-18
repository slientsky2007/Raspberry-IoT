#!/usr/bin/env python3
import os
import socket
import sys
import time
from BASICDEF import bytes2human

try:
	import psutil
except ImportError:
	print("The psutil library was not found. Run 'sudo -H pip install psutil' to install it.")
	sys.exit()

class system():
	def __init__(self, iface):
		self.IFACE_INIT = iface
		self.SEND_INIT = ""
		self.RECV_INIT = ""

	def get_RT_network_traffic(self, timesleep):
		new_recv,new_send = self.get_net_TxRx(self.IFACE_INIT)
		recv_data = bytes2human((new_recv - self.RECV_INIT)/timesleep)
		send_data = bytes2human((new_send - self.SEND_INIT)/timesleep)
		self.RECV_INIT = new_recv
		self.SEND_INIT = new_send
		return "Tx %s,  Rx %s" % \
				(send_data, recv_data)

	def get_net_TxRx(self):
		stat = psutil.net_io_counters(pernic=True)[self.iface]
		send = stat.bytes_sent
		recv = stat.bytes_recv
		return (recv, send)
	
	def get_mem_usage(self):
		usage = psutil.virtual_memory()
		return "Mem: %s %.0f%% %s free" \
			% (bytes2human(usage.total), usage.percent, bytes2human(usage.free))
					
	def getDate(self):
		dt = datetime.now()
		return dt.strftime( '%Y-%m-%d' )

	def getTime(self):
		dt = datetime.now()
		return dt.strftime( '%H:%M:%S %p' )

	def getDateTime(self):
		dt = datetime.now()
		return dt.strftime( '%x %H:%M:%S %p' )

	  
	def getIP(self):  
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   
		return socket.inet_ntoa(fcntl.ioctl(   
			s.fileno(),   
			0x8915,  # SIOCGIFADDR   
			struct.pack('256s', self.IFACE_INIT[:15].encode('utf-8'))   
		)[20:24])
	


	