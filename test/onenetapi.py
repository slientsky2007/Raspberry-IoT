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

"""
-------------------------------------------------
datastream_id=a,b,c //查询的数据流，多个数据流之间用逗号分隔（可选）
start=2015-01-10T08:00:35 //提取数据点的开始时间（可选）
end=2015-01-10T08:00:35 //提取数据点的结束时间（可选）
duration=3600 //查询时间区间（可选，单位为秒）
start+duration：按时间顺序返回从start开始一段时间内的数据点
end+duration：按时间倒序返回从end回溯一段时间内的数据点
limit=100 //限定本次请求最多返回的数据点数，0<n<=6000（可选，默认1440）
cursor= //指定本次请求继续从cursor位置开始提取数据（可选）
sort=DESC | ASC //值为DESC|ASC时间排序方式，DESC:倒序，ASC升序，默认升序
</n<=6000（可选，默认1440）
-------------------------------------------------
"""
def test_get_datapoints(rPi, datastream_id, limit):
	rPi.set_get_data('datastream_id', datastream_id)
	rPi.set_get_data('limit', limit)
	rPi.set_get_data('sort', 'ASC')
	r = rPi.get_datapoints()
	print(r.url + ' -- ', end='')
	print(r.status_code)
	try:
		s = eval(r.text)
	except AttributeError:
		print('get_datapoints failed')
		return False
	# print(s)
	data = s['data']['datastreams'][0]
	for n in data['datapoints']:
		print(n['at'])
		print(n['value'])
		print('------------------')
		
def test_get_dataflow(rPi, datastream_ids):
	# 测试get 数据流
	rPi.set_get_data('datastream_ids', datastream_ids)
	r = rPi.get_dataflow()
	s = eval(r.text)
	for n in s['data']:
		print(n['update_at'])
		print(n['current_value'])
		
def test_repost(rPi, datastream_ids):
# 测试post 数据流
	#初始化计数器，用于控制循环次数
	num = 0
	while True:
		if num < 10:
			# 构建RESTful data部分数据
			rPi.set_post_data_flow(datastream_ids, random.randint(1, 100))
			# print(rPi.dict)
			# 上传数据到OneNet
			r = rPi.post_data_flow()
			num +=1
			time.sleep(5)
			
			print('1',20 * '*')
			# print(r.url)
			# print(r.headers)
			print(r.text)
			print('2',20 * '*')
			
		# 计数结束，退出循环
		else:break
		
def main(argv):
	m = argv[1:]
	#检查是否有参数传入
	if m == []:
		print("Parameters Not exsit! You can't use OneNet API")
	#检查配置文件是否存在
	elif (os.path.isfile(argv[1]) == False):
		print("file: "+ argv[1] + " not exist! You can't use OneNet API")
	else:
		#捕获异常，检查是否对应配置文件中的参数
		try:
			_deviceid = BasicDef.get_pares_info(argv, 'deviceid')
			# print('_deviceid: ', _deviceid)
			_apikey = BasicDef.get_pares_info(argv, 'apikey')
			# print('_apikey: ', _apikey)
		except KeyError as e:
			print("--device=%s is not exsit!" % e)
			return

		#检查没有问题，将配置文件中的_deviceid，_apikey 设置为全局可获取
		BasicDef.set_device_id(_deviceid)
		BasicDef.set_apikey(_apikey)
		#初始化onenet对象
		rPi = OneNetApi()
		
		#上传10个数据点到数据流Test1/Test2
		# test_repost(rPi, 'Test1')
		
		#读取最新上传数据流的数据点
		# test_get_dataflow(rPi, 'Test1')
		
		#读取某个数据流中最近的10个数据点
		test_get_datapoints(rPi, 'Test1', 10)

# if __name__ == "__main__":
	# try:
		# main(sys.argv)
	# except KeyboardInterrupt:
		# pass
