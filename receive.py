#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import datetime

import serial

print('==> starting receive.py')

# file storing data
filename = '/tmp/sensor.log'

serialArduino = serial.Serial('/dev/ttyACM0', 57600)

while 1:

    # verification if data are received from serial
    while serialArduino.inWaiting() == 0:
        pass

    valueRead = serialArduino.readline()

    FileTemp = open(filename, 'wb')
    FileTemp.write(valueRead)
    FileTemp.close()

    time.sleep(2)
