import groveGetter
import requests
import json
import time

packet = {}
grove = groveGetter.groveGetter()

while True:
	grove.update()
	packet["p_brightness"] = grove.dataDict["p_brightness"]
	packet["p_temperature"] = grove.dataDict["p_temperature"]
	packet["p_humidity"] = grove.dataDict["p_humidity"]
	packet["p_pressure"] = grove.dataDict["p_pressure"]
	packet["p_lat"] = grove.dataDict["p_lat"]
	packet["p_lon"] = grove.dataDict["p_lon"]
	packet["p_alt"] = grove.dataDict["p_alt"]

	print "[logger] packet =>"
	print "    brightness : " + str(packet["p_brightness"])
	print "    temperature: " + str(packet["p_temperature"])
	print "    humidity   : " + str(packet["p_humidity"])
	print "    pressure   : " + str(packet["p_pressure"])
	print "    latitude   : " + str(packet["p_lat"])
	print "    longitude  : " + str(packet["p_lon"])
	print "    altitude   : " + str(packet["p_alt"])

	try:
		response = requests.post("http://127.0.0.1:51966/sensor", json.dumps(packet))
		print "[logger] post: " + str(response.status_code)
 	except requests.exceptions.ConnectionError:
		print "[logger] post: barista-rasp-server is down"
	except requests.exceptions.RequestException:
		print "[logger] post: unknown error"

	time.sleep(10)
