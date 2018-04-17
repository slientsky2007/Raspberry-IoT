#!/usr/bin/env python3  
import sys, time, os
try:
	import psutil
except ImportError:
	print("The psutil library was not found. Run 'sudo -H pip install psutil' to install it.")
	sys.exit()

class nettest:
	IFACE_INIT = ""
	RECV_INIT = 0
	SEND_INIT = 0
	def __init__(self, iface):
		self.IFACE_INIT = iface
		self.SEND_INIT, self.RECV_INIT = self.get_net_TxRx(iface)
		
	def bytes2human(self, n):
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

	def network(self, timesleep):
		new_recv,new_send = self.get_net_TxRx(self.IFACE_INIT)
		recv_data = self.bytes2human((new_recv - self.RECV_INIT)/timesleep)
		send_data = self.bytes2human((new_send - self.SEND_INIT)/timesleep)
		self.RECV_INIT = new_recv
		self.SEND_INIT = new_send
		return "Tx %s,  Rx %s" % \
				(send_data, recv_data)

	def get_net_TxRx(self, iface):
		stat = psutil.net_io_counters(pernic=True)[iface]
		send = stat.bytes_sent
		recv = stat.bytes_recv
		return (recv, send)
	


	