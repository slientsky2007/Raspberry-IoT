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
    def __init__(self, deviceid, apikey):
        # 设备ID
        self.DEVICEID = deviceid
        # 数据流名称
        self.SENSORID = ''
        # 数值
        self.VALUE = 0
        # APIKEY
        self.APIKEY = apikey

    def set(self, sensorid, value):
        self.SENSORID = sensorid
        self.VALUE = value

    def post(self):
        # dt = datetime.datetime.now()
        # date = dt.strftime( '%x %H:%M:%S %p' )
        url = 'http://api.heclouds.com/devices/%s/datapoints' % (self.DEVICEID)
        dict = {"datastreams": [{"id": "TEMP", "datapoints": [{"value": 50}]}]}
        dict['datastreams'][0]['id'] = self.SENSORID
        dict['datastreams'][0]['datapoints'][0]['value'] = self.VALUE

        s = json.dumps(dict)
        headers = {
            "api-key": self.APIKEY,
            "Connection": "close",
            # "Date": date
        }
        try:
            r = requests.post(url, headers = headers, data = s)
        except RequestException:
            return False

        return r


def main():
    DEVICEID = '29577383'
    SENSORID = 'Test'
    VALUE = 50
    APIKEY = 'QzCP2X7dyYVCg=loObHOt6L6hQ8='

    rPi = onenet(DEVICEID, APIKEY)

    while True:
        VALUE += 5
        if VALUE < 55:
            rPi.set(SENSORID, VALUE)
            r = rPi.post()

            print(r.headers)
            print('1',20 * '*')
            print(r.text)
            print('2',20 * '*')
            time.sleep(5)
        else:break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass