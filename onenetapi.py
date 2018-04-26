#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    onenetapi
   Description :  OneNet平台操作处理
   Author :       Slientsky
   date：         2018-04-23
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
import random

from basicdef import BasicDef

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
	reload(sys)
	sys.setdefaultencoding(defaultencoding)

class OneNetApi():
	def __init__(self):
		# 设备ID
		self.DEVICEID = BasicDef.get_device_id()
		# APIKEY
		self.APIKEY = BasicDef.get_apikey()
		
		self.num = 0
		self.dict = {"datastreams": []}
		self.SENSORID = []
		self.payload = {}

	#设置上传的数据流sensorid，数据点值value
	def set_post_data_flow(self, sensorid, value):
		d = {"id": "TEMP", "datapoints": [{"value": 50}]}
		d['id'] = sensorid
		d['datapoints'][0]['value'] = value
		self.dict['datastreams'].append(d)

	#提交数据流的数据点
	def post_data_flow(self):
		url = "http://api.heclouds.com/devices/%s/datapoints" % (self.DEVICEID)
		
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
		
	def set_get_data(self, keys, sensorid):
		if self.payload.get(keys) == None:
			self.payload[keys] = sensorid
		else:
			s = ',' + sensorid
			self.payload[keys] += s
		# print(self.payload)
	
	#查询数据流
	def get_dataflow(self):
		url = "http://api.heclouds.com/devices/%s/datastreams" % (self.DEVICEID)
		headers = {
			"api-key": self.APIKEY,
			"Connection": "close",
		}
		try:
			r = requests.get(url, headers=headers, params=self.payload, timeout=1)
		except:
			print("get_data_flow failed")
			return False
		finally: self.payload = {}
		return r
	
	#查询一段时间内的数据点
	def get_datapoints(self):
		url = "http://api.heclouds.com/devices/%s/datapoints" % (self.DEVICEID)
		headers = {
			"api-key": self.APIKEY,
			"Connection": "close",
		}
		try:
			r = requests.get(url, headers=headers, params=self.payload, timeout=1)
		except:
			print("get_data_flow failed")
			return False
		finally: self.payload = {}
		return r