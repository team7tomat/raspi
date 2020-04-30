#!/usr/bin/env python
# coding=utf-8

from socket import *
from time import sleep
import json
import picamera
import os

def main():
	with picamera.PiCamera() as camera:
		camera.resolution = (1920, 1080)
		#mac = os.popen("cat /sys/class/net/eth0/address | tr : _").read().split('\n')[0]
		#filename = mac + ".jpg"
		server_socket = socket(AF_INET, SOCK_STREAM)
		server_port = 1337

		server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

		server_socket.bind(('', server_port))
		server_socket.listen(1)
		print ('The TCP server is ready to receive')

		while True:
			data = bytes("", "utf-8")
			connection_socket, address = server_socket.accept()

			while True:
				new_data = connection_socket.recv(4096).decode()

				if new_data == "image":
					camera.capture("abc123.jpg")

					with open("abc123.jpg", 'rb') as file:
						print("sending file")
						connection_socket.sendall(file.read())
						connection_socket.close()
					break # from while-loop

				if new_data == "sunlight":
					print(new_data)
					with open ("24h_info.txt", 'rb+') as file:
						print("sending sunlight data")
						connection_socket.sendall(file.read())
						connection_socket.close()
						file.seek(0)
						file.truncate()
					break # from while-loop

				if new_data[:6] == "config":
					print(new_data)
					conf_data = new_data[6:]
					print(conf_data)
					with open("conf.txt",'w+') as file: # save to file
						file.write(conf_data)
					break # from while-loop

				if new_data[:8] == "tomatoes":
					print(new_data)
					tomato_data = new_data[8:]
					print(tomato_data)
					with open("tomato.txt",'w+') as file: # save to file
						file.write(tomato_data)
					break # from while-loop


if __name__ == "__main__":
	main()

