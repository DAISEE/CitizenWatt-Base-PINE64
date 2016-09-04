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

    print('-> 1. ' + str(datetime.datetime.now()))
    valueRead = serialArduino.readline()

    print('-> 2. ' + str(datetime.datetime.now()))
    FileTemp = open(filename, 'wb')
    FileTemp.write(valueRead)
    FileTemp.close()

    print('-> 3. ' + str(datetime.datetime.now()))

    time.sleep(2)

