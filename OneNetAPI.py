#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     onenetPostTest
   Description :
   Author :       Slientsky
   date：          2018-04-23
-------------------------------------------------
   Change Activity:
                   2018-04-23
-------------------------------------------------
"""
import datetime
import time
import requests
import json
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
	reload(sys)
	sys.setdefaultencoding(defaultencoding)

class onenet():
	def __init__(self, deviceid='29577383', apikey='QzCP2X7dyYVCg=loObHOt6L6hQ8='):
		# 设备ID
		self.DEVICEID = deviceid
		# 数据流名称
		self.SENSORID = ''
		# 数值
		self.VALUE = 0
		# APIKEY
		self.APIKEY = apikey
		
		self.num = 0
		self.dict = {"datastreams": []}

	def set(self, sensorid, value):
		self.SENSORID = sensorid
		self.VALUE = value
		
		d = {"id": "TEMP", "datapoints": [{"value": 50}]}
		d['id'] = self.SENSORID
		d['datapoints'][0]['value'] = self.VALUE
		self.dict['datastreams'].append(d)

	def post(self):
		url = 'http://api.heclouds.com/devices/%s/datapoints' % (self.DEVICEID)
		s = json.dumps(self.dict)
		headers = {
			"api-key": self.APIKEY,
			"Connection": "close",
		}
		try:
			r = requests.post(url, headers = headers, data = s)
		except requests.RequestException:
			return False
		finally:
			self.dict = {"datastreams": []}
		# print(r.text)
		return r