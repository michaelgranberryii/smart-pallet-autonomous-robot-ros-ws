#!/usr/bin/env python
from smbus2 import SMBus #I2C
import time #Delay

class Sonar:
	def __init__(self, i2cAddress):
		self.i2cAddress = i2cAddress
		self.writeRangeCmd = 0x51 #Write range Command. 81 in decimal
		self.initRead = 0xe1 #Initiate read. 225 in decimal
		self.delay1 = 0.1 #100ms

	def read_range(self):
		try:
			i2cbus = SMBus(1)
			i2cbus.write_byte_data(self.i2cAddress, 0, self.writeRangeCmd) #Write the range command byte.
			time.sleep(self.delay1)
			rawData = i2cbus.read_word_data(self.i2cAddress, self.initRead) #Initiate a read at the sensor address. Word = 2bytes.
			rangeValue = (rawData >> 8) & 0xff #Right shift 8-bits. Mask with 0x00ff.
			i2cbus.close()
			return rangeValue
		except IOError as err:
			print(err)

