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
import sys, os
import random

from basicdef import BasicDef

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
	reload(sys)
	sys.setdefaultencoding(defaultencoding)

class onenet():
	def __init__(self):
		# 设备ID
		self.DEVICEID = BasicDef.get_device_id()
		# 数据流名称
		self.SENSORID = ''
		# 数值
		self.VALUE = 0
		# APIKEY
		self.APIKEY = BasicDef.get_apikey()
		
		self.num = 0
		self.dict = {"datastreams": []}

	def set(self, sensorid, value):
		self.SENSORID = sensorid
		self.VALUE = value
		
		d = {"id": "TEMP", "datapoints": [{"value": 50}]}
		d['id'] = self.SENSORID
		d['datapoints'][0]['value'] = self.VALUE
		self.dict['datastreams'].append(d)

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
		
def main(argv):
	m = argv[1:]
	#检查是否有参数传入
	if m == []:
		print("Parameters Not exsit! Data won't post to OnetNet")
	#检查配置文件是否存在
	elif (os.path.isfile(argv[1]) == False):
		print("file: "+ argv[1] + " not exist! Data won't post to OneNet")
	else:
		#捕获异常，检查是否对应配置文件中的参数
		try:
			_deviceid = BasicDef.get_pares_info(argv, 'deviceid')
			print('_deviceid: ', _deviceid)
			_apikey = BasicDef.get_pares_info(argv, 'apikey')
			print('_apikey: ', _apikey)
		except KeyError as e:
			print("--device=%s is not exsit!" % e)
			return

		#检查没有问题，将配置文件中的_deviceid，_apikey 设置为全局可获取
		BasicDef.set_device_id(_deviceid)
		BasicDef.set_apikey(_apikey)
		#初始化onenet对象
		rPi = onenet()
		#初始化计数器，用于控制循环次数
		num = 0

		while True:
			if num < 1:
				#构建RESTful data部分数据
				rPi.set("Test1", random.randint(1, 100))
				rPi.set("Test2", random.randint(1, 100))
				# print(rPi.dict)
				#上传数据到OneNet
				r = rPi.post_data_flow()
				num +=1
				# print(r.headers)
				# print('1',20 * '*')
				# print(r.text)
				# print('2',20 * '*')
				time.sleep(5)
			#计数结束，退出循环
			else:break

if __name__ == "__main__":
	try:
		main(sys.argv)
	except KeyboardInterrupt:
		pass