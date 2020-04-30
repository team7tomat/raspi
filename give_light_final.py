import datetime
from time import sleep
from get_sunlight import read_light
from multipwm_led import Armature
#from get_daytime import get_daytime
import pigpio
import json
import os

max_colors = { "blue":4211, "white":16725, "hred":41335 }

def do_shit(ratios, pins, lux_goal, intensity):
	armature = Armature(int(pins["pinw"]), int(pins["pinb"]), int(pins["pinhr"]), int(pins["pinlr"]))
	functions = { "blue": armature.set_blue, "white": armature.set_white, "hred": armature.set_hred }

# this check needs to be done when the user puts the ratios in the GUI
#	x = 0
#	for key in max_colors:
#		x += max_colors[key] * ratios[key]
#	x = lux_goal / x
#	for value in ratios.values():
#		if x * value > 1:
#			print("faulty ratios")
#			return

	current_lux = read_light()
	artificial_light = lux_goal - current_lux if current_lux < lux_goal else 0

	if artificial_light != 0:
		x = 0
		for key in max_colors:
			x += max_colors[key]*ratios[key]
		x = artificial_light / x

		for key, value in ratios.items():
			func = functions.get(key)
			func(x*value*100)
			#print(x*value*100)

	now = datetime.datetime.now()
	with open("24h_info.txt", "a+", os.O_NONBLOCK) as file:
		file.write(str(int(current_lux)) + ', ')
		month = str(now.month).zfill(2)
		day = str(now.day).zfill(2)
		hour = str(now.hour).zfill(2)
		minute = str(now.minute).zfill(2)
		file.write("{}-{}-{} {}:{}:00".format(now.year, month, day, hour, minute) + '\n')

	sleep(10)
	armature.end()

def time_logic(now, daybegin, dayend, nightbegin, nightend, ratios, pins, lux_goal, intensity):
	while now < daybegin or now > dayend: # it is between nightend and daybegin
		sleep(600)
		#print("now < daybegin", "\tnow: ", now, "\tdaybegin: ", daybegin)
		#sleep(0.5)
		#now += datetime.timedelta(minutes=20)

	while now < dayend: # it is day
		#print("now < dayend", "\tnow: ", now, "\tdayend: ", dayend)
		#sleep(0.5)
		#now += datetime.timedelta(minutes=20)
		do_shit(ratios, pins, lux_goal, intensity)


def main():
	while True:
		now = datetime.datetime.now()
		nightbegin, nightend = None, None
		daybegin, dayend = ({ "hour" : 6, "minute" : 0 }, { "hour" : 22, "minute" : 0 })
		daybegin = now.replace(hour=daybegin["hour"], minute=daybegin["minute"])
		dayend = now.replace(hour=dayend["hour"], minute=dayend["minute"])

		ratios = None
		pins = None
		lux_goal = None
		intensity = None

		with open("conf.txt", 'r') as file:
			conf = json.loads(file.read())
			ratios = {"blue": conf["blue"], "white": conf["white"], "hred": conf["hred"]}
			pins = {"pinw": conf["pinw"], "pinb": conf["pinb"], "pinhr": conf["pinhr"], "pinlr": conf["pinlr"]}
			lux_goal = conf["lux"]
			intensity = conf["intensity"]
			nightbegin = conf["nightbegin"].split(':')
			nightbegin = now.replace(hour=int(nightbegin[0]), minute=int(nightbegin[1]))
			nightend = conf["nightend"].split(':')
			nightend = now.replace(hour=int(nightend[0]), minute=int(nightend[1]))
			if nightend.hour < nightbegin.hour:
				nightend += datetime.timedelta(days=1)

		try:
			with open ("tomato.txt", 'r') as file:
				tomatoes = json.loads(file.read())
				print(tomatoes)
				exit()
				if int(tomatoes["non_ripe"]) == 0 and int(tomatoes["ripe"]) != 0:
					sleep(600)
				else:
					time_logic(now, daybegin, dayend, nightbegin, nightend, ratios, pins, lux_goal, intensity)
		except FileNotFoundError:
			time_logic(now, daybegin, dayend, nightbegin, nightend, ratios, pins, lux_goal, intensity)



if __name__ == "__main__":
	main()
