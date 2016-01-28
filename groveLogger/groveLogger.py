# -*- coding: utf-8 -*-
import time
import logWriter

log = logWriter.logWriter()
log.init()

while True:
	log.makeLog()
	log.post()
	time.sleep(10)
