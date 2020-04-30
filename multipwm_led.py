#import RPi.GPIO as GPIO
import pigpio
import time

class Armature:
	def __init__(self, white, red1, red2, blue):
		#print("Init")
		self.pi = pigpio.pi()
		self.white = white	# gpio 12
		self.hred = red1	# gpio 13
		self.lred = red2	# gpio 16
		self.blue = blue	# gpio 19
		# set output
		self.pi.set_mode(self.white, pigpio.OUTPUT)
		self.pi.set_mode(self.hred, pigpio.OUTPUT)
		self.pi.set_mode(self.lred, pigpio.OUTPUT)
		self.pi.set_mode(self.blue, pigpio.OUTPUT)
		# set 200hz pwm
		self.pi.set_PWM_frequency(self.white, 200)
		self.pi.set_PWM_frequency(self.hred, 200)
		self.pi.set_PWM_frequency(self.lred, 200)
		self.pi.set_PWM_frequency(self.blue, 200)


	# Translate % value to 8bit
	def perc_trans(self, arg):
		if int(arg) > 100:
			return 255
		if int(arg) < 0:
			return 0
		return int(float(arg) * 2.55)

	# Set % color intensity
	def set_white(self, arg):
		self.pi.set_PWM_dutycycle(self.white, self.perc_trans(arg))
	def set_hred(self, arg):
		self.pi.set_PWM_dutycycle(self.hred, self.perc_trans(arg))
	def set_lred(self, arg):
		self.pi.set_PWM_dutycycle(self.lred, self.perc_trans(arg))
	def set_blue(self, arg):
		self.pi.set_PWM_dutycycle(self.blue, self.perc_trans(arg))

	def turn_off_lights(self):
		self.set_white(0)
		self.set_hred(0)
		self.set_lred(0)
		self.set_blue(0)

	def end(self):
		self.turn_off_lights()
		self.pi.stop()


# main
if __name__ == "__main__":
	print("Hello")
	# current gpio_pins are 12, 13, 16, 19
	test = Armature(12,13,16,19)

	switcher = {
	"white": test.set_white,
	"hred": test.set_hred,
	"lred": test.set_lred,
	"blue": test.set_blue
	}

	stop = False
	while (stop == False):
		str = input("What do? ")
		spl = str.split(" ", 1) # 2 elements
		if spl[0] == "stop":
			stop = True
		else:
			func = switcher.get(spl[0], lambda: "Problem")
			func(spl[1])
	#set_hred(10)
	test.end()
