#!/usr/bin/python
import smbus

# Define some constants from the datasheet
DEVICE     = 0x23 # Default device I2C address
POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value
ONE_TIME_HIGH_RES_MODE = 0x20

bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def convert_to_number(data):
	# Simple function to convert 2 bytes of data into a decimal number
	return ((data[1] + (256 * data[0])) / 1.2)

def read_light(addr=DEVICE):
	data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE)
	return convert_to_number(data)

def main():
	print(read_light())

if __name__ == "__main__":
	main()
