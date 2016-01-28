# -*- coding: utf-8 -*-

import groveGetter
import os
import datetime
import locale
import json
import requests

class logWriter:
	getter = groveGetter.groveGetter()
	lastLog = {}

	def init(self):
		self.getter.initialize()

	def makeLog(self):
		self.getter.reflesh()
		d = datetime.datetime.today()
		self.lastLog["p_brightness"] = self.getter.dataDict["brightness"]
		self.lastLog["p_temperature"] = self.getter.dataDict["temp"]
		self.lastLog["p_humidity"] = self.getter.dataDict["humid"]
		self.lastLog["p_pressure"] = self.getter.dataDict["pressure"]
		self.lastLog["p_lon"] = self.getter.dataDict["Longtitude"]
		self.lastLog["p_lat"] = self.getter.dataDict["Latitude"]
		self.lastLog["p_alt"] = self.getter.dataDict["Altitude"]
        
		print "=== Log ===" + d.strftime("%H:%M:%S")
		print "Brightness :" + str(self.lastLog["p_brightness"])
		print "Temperature:" + str(self.lastLog["p_temperature"])
		print "Humidity   :" + str(self.lastLog["p_humidity"])
		print "Pressure   :" + str(self.lastLog["p_pressure"])
		print "Latitude   :" + str(self.lastLog["p_lat"])
		print "Longtitude :" + str(self.lastLog["p_lon"])
		print "Altitude   :" + str(self.lastLog["p_alt"])

	def post(self):
		try:
			requests.post('http://127.0.0.1:51966/sensor', json.dumps(self.lastLog))
		except requests.exceptions.ConnectionError:
			print "POST Request connection error"
