#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Zhihao Zheng (Arthur)

import socket
import struct
import sys
import time
from ctypes import *

lib = CDLL("./lx16a.so")

class ServoMotor():
	def __init__(self, filename):
		self.filename = filename

	def IO_Init(self):
		IO1 = lib.IO_init(c_char_p(self.filename.encode('ascii')))
		return IO1

	def setServoID(self, id, new_id):
		lib.setServoID(id,new_id)

	def move(self, id, position, time):
		lib.move(id, position, time)

	def movePrepare(self, id, position, time):
		lib.movePrepare(id, position, time)

	def getPreparedMove(self, id):
		data = lib.getPreparedMove(id)
		pos = data >> 16
		time = data & 0xffff
		if pos > 1000 or data < 0:
			return False
		else:
			return pos, time

	def moveStart(self,id):
		lib.moveStart(id)

	def moveStop(self, id):
		lib.moveStop(id)

	def setPositionOffset(self, id, deviation):
		lib.setPositionOffset(id, deviation)

	def getPositionOffset(self, id):
		deviation = lib.getPositionOffset(id)
		if abs(deviation) > 125:
			return False
		else:
			return deviation

	def setPositionLimits(self, id, minPos, maxPos):
		lib.setPositionLimits(id, minPos, maxPos)

	def getPositionLimits(self, id):
		data = lib.getPositionLimits(id)
		minPos = data >> 16
		maxPos = data & 0xffff
		if minPos > 1000 or maxPos > 1000 or data < 0:
			return False
		else:
			return minPos, maxPos

	def savePositionOffset(self, id):
		lib.savePositionOffset(id)

	def setVoltageLimits(self, id, minVolt, maxVolt):
		lib.setVoltageLimits(id, minVolt, maxVolt)

	def getVoltageLimits(self, id):
		data = lib.getVoltageLimits(id)
		minVolt = data >> 16
		maxVolt = data & 0xffff
		if minVolt > 12500 or data < 0:
			return False
		else:
			return minVolt, maxVolt

	def setMaxTemp(self, id, temp):
		lib.setMaxTemp(id, temp)

	def getMaxTemp(self, id):
		temp = lib.getMaxTemp(id)
		if temp > 125 or temp < 0:
			return False
		else:
			return temp

	def getTemp(self, id):
		temp = lib.getTemp(id)
		if temp > 125 or temp < 0:
			return False
		else:
			return temp

	def getVoltage(self, id):
		vol = lib.getVoltage(id)
		if vol > 19000 or vol < 0:
			return False
		else:
			return vol

	def motorOn(self, id):
		lib.motorOn(id)

	def motorOff(self, id):
		lib.motorOff(id)

	def isMotorOn(self, id):
		status = lib.isMotorOn(id)
		if status > 1 or status < 0:
			return False
		else:
			return status

	def LEDOn(self, id):
		lib.setLED(id,1)

	def LEDOff(self, id):
		lib.setLED(id,0)

	def isLEDOn(self, id):
		status = lib.isLEDOn(id)
		if status > 1 or status < 0:
			return False
		else:
			return status

	def setLEDErrors(self, id, error):
		lib.setLEDErrors(id, error)

	def getLEDErrors(self, id):
		error = lib.getLEDErrors(id)
		if error > 7 or error < 0:
			return False
		else:
			return error

	def setServoMode(self, id):
		lib.setServoMode(id)

	def getMode(self, id):
		mode = lib.getMode(id)
		if mode > 1 or mode < 0:
			return False
		else:
			return mode

	def setSpeed(self, id, speed):
		lib.setSpeed(id, speed)

	def readSpeedSetting(self, id):
		speed = lib.getSpeedSetting(id)
		if abs(speed) > 1000:
			return False
		else:
			return speed

	def readPosition(self, id):
		position = lib.posRead(id)
		if abs(position) > 2000:
			return False
		else:
			return position

	pass