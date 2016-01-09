
from grove_i2c_barometic_sensor_BMP180 import BMP085
import RPi.GPIO as GPIO
import grovepi
import smbus
import time
import math
import sys
import serial

pins_dht = 4
pins_bright = 14 # Pin 14 is A0 Port.

class groveGetter:
	
	dataDict = {}
	bmp = None
	ser = None
	inp=[]
	GGA=[]

	def decimal_degrees(self, raw_degrees):
		degrees = float(raw_degrees) // 100
		d = float(raw_degrees) % 100 / 60
		return degrees + d
	
	def initialize(self):
		grovepi.pinMode(pins_bright,"INPUT")
		self.ser = serial.Serial('/dev/ttyAMA0', 9600, timeout = 0)
		self.ser.flush()
		self.bmp = BMP085(0x77, 1)
		rev = GPIO.RPI_REVISION
		if rev == 2 or rev == 3:
			bus = smbus.SMBus(1)
		else:
			bus = smbus.SMBus(0)

	def reflesh(self):
		[temp,humidity] = grovepi.dht(pins_dht,1)
		pressure = self.bmp.readPressure()
		
		self.dataDict["brightness"] = 0
		self.dataDict["temp"] = 0
		self.dataDict["humid"] = 0
		self.dataDict["pressure"] = 0
		try:
			self.dataDict["brightness"] = grovepi.analogRead(pins_bright)

		except IOError:
			print ("analog Error")

		self.dataDict["temp"] = temp
		self.dataDict["humid"] = humidity
		self.dataDict["pressure"] = pressure / 100.0

		#GPS
		cnt = 0
		gpsSuccess = False
		print "start GPS..."
		while (cnt < 30):
			self.inp = self.ser.readline()
			if self.inp[:6] == '$GPGGA':
				gpsSuccess = True
				break
			time.sleep(0.1)
			cnt = cnt + 1
		try:
			ind=self.inp.index('$GPGGA', 5, len(self.inp))
			self.inp = self.inp[ind:]
		except ValueError:
			print "Value error"
		
		self.dataDict["Altitude"] = 0
		self.dataDict["Latitude"] = 0
		self.dataDict["Longtitude"] = 0

		if gpsSuccess:
			self.GGA = self.inp.split(",")
			t = self.GGA[1]
			lat = self.GGA[2]
			lat_ns = self.GGA[3]
			long = self.GGA[4]
			long_ew = self.GGA[5]
			fix = self.GGA[6]
			sats = self.GGA[7]
			alt = self.GGA[9]
		
			if lat.replace(".","",1).isdigit():
				lat = self.decimal_degrees(float(lat))
				#lat = lat / 100.0
				if lat_ns == "S":
					lat = -lat
		
			if long.replace(".","",1).isdigit():
				long = self.decimal_degrees(float(long))
				#long = long / 100.0
				if long_ew == "W":
					long = -long

			self.dataDict["Altitude"] = alt
			self.dataDict["Latitude"] = lat
			self.dataDict["Longtitude"] = long
