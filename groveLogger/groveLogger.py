# -*- coding: utf-8 -*-
import time
import logWriter

log = logWriter.logWriter()

log.init()
log.load()

while True:
	log.makeLog()
	log.save()
	log.post()
	time.sleep(10)
