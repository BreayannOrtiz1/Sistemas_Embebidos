#!/bin/python3

import wiringpi
import time

wiringpi.wiringPiSetup()
#wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(1,1)
#wiringpi.digitalWrite(2,1)


while(1):
	wiringpi.digitalWrite(1,1)
	#time.sleep(1)
	wiringpi.digitalWrite(1,0)
	#time.sleep(1)

