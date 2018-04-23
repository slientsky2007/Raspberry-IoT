#!/usr/bin/env python3
import fcntl
import struct
import os
import socket
import sys
import time
import datetime
from BASICDEF import basic

try:
	import psutil
except ImportError:
	print("The psutil library was not found. Run 'sudo -H pip install psutil' to install it.")
	sys.exit()

class system():
	def __init__(self, iface):
		self.IFACE_INIT = iface
		#上一次时间间隔时网络发送总流量和接受总流量
		self.SEND_INIT = 0
		self.RECV_INIT = 0
		#当前时间间隔内的发送和接受流量(计算得到的实时网络流量)
		self.Rx = 0
		self.Tx = 0

	def get_RT_network_traffic(self, timesleep):
		new_recv,new_send = self.get_net_TxRx()
		self.Rx = (new_recv - self.RECV_INIT)/timesleep
		self.Tx = (new_send - self.SEND_INIT)/timesleep
		recv_data = basic.bytes2human(Rx)
		send_data = basic.bytes2human(Tx)
		self.RECV_INIT = new_recv
		self.SEND_INIT = new_send
		return "Tx %s,  Rx %s" % \
				(send_data, recv_data)

	def get_net_TxRx(self):
		stat = psutil.net_io_counters(pernic=True)[self.IFACE_INIT]
		send = stat.bytes_sent
		recv = stat.bytes_recv
		return (recv, send)
	
	def get_mem_usage(self):
		usage = psutil.virtual_memory()
		return "Mem: %s %.0f%% %s free" \
			% (basic.bytes2human(usage.total), usage.percent, basic.bytes2human(usage.free))
					
	def getDate(self):
		dt = datetime.datetime.now()
		return dt.strftime( '%Y-%m-%d' )

	def getTime(self):
		dt = datetime.datetime.now()
		return dt.strftime( '%H:%M:%S %p' )

	def getDateTime(self):
		dt = datetime.datetime.now()
		return dt.strftime( '%x %H:%M:%S %p' )

	  
	def getIP(self):  
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   
		return socket.inet_ntoa(fcntl.ioctl(   
			s.fileno(),   
			0x8915,  # SIOCGIFADDR   
			struct.pack('256s', self.IFACE_INIT[:15].encode('utf-8'))   
		)[20:24])
	


	