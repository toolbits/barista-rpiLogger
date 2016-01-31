import grovepi
import serial
from grove_i2c_barometic_sensor_BMP180 import BMP085
import RPi.GPIO as GPIO
import smbus
import time

pins_dht = 4
pins_brightness = 14 # Pin 14 is A0 Port.

class groveGetter:
    dataDict = {}
    serial = None
    bmp = None

    def __init__(self):
        self.dataDict["p_brightness"] = 0
        self.dataDict["p_temperature"] = 0
        self.dataDict["p_humidity"] = 0
        self.dataDict["p_pressure"] = 0
        self.dataDict["p_lat"] = 0
        self.dataDict["p_lon"] = 0
        self.dataDict["p_alt"] = 0

        grovepi.pinMode(pins_brightness, "INPUT")

        self.serial = serial.Serial("/dev/ttyAMA0", 9600, timeout = 0)
        self.serial.flush()

        self.bmp = BMP085(0x77, 1)
        if GPIO.RPI_REVISION == 2 or GPIO.RPI_REVISION == 3:
            smbus.SMBus(1)
        else:
            smbus.SMBus(0)

    def update(self):
        try:
            brightness = grovepi.analogRead(pins_brightness)
            self.dataDict["p_brightness"] = brightness
        except:
            print "[logger] update: analogRead error"
        try:
            [temperature, humidity] = grovepi.dht(pins_dht, 1)
            self.dataDict["p_temperature"] = temperature
            self.dataDict["p_humidity"] = humidity
        except:
            print "[logger] update: dht error"
        try:
            pressure = self.bmp.readPressure()
            self.dataDict["p_pressure"] = pressure / 100.0
        except:
            print "[logger] update: readPressure error"

        self.serial.flush()
        while True:
            gps = self.serial.readline()
            if gps[:6] == "$GPGGA":
                break;
            time.sleep(0.1)
        try:
            index = gps.index("$GPGGA", 5, len(gps))
            gps = gps[index:]
        except:
            pass
        gga = gps.split(",")
        if len(gga) > 9:
            lat = gga[2]
            lat_ns = gga[3]
            lon = gga[4]
            lon_ew = gga[5]
            alt = gga[9]
            if lat.replace(".", "", 1).isdigit():
                lat = self.decimal_degrees(float(lat))
                if lat_ns == "S":
                    lat = -lat
            if lon.replace(".", "", 1).isdigit():
                lon = self.decimal_degrees(float(lon))
                if long_ew == "W":
                    lon = -lon
            self.dataDict["p_lat"] = lat
            self.dataDict["p_lon"] = lon
            self.dataDict["p_alt"] = alt
    def decimal_degrees(self, raw_degrees):
        degrees = float(raw_degrees) // 100
        d = float(raw_degrees) % 100 / 60
        return degrees + d
