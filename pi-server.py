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

		server_port = 1337
		# Create socket
		server_socket = socket(AF_INET, SOCK_STREAM)
		server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		server_socket.bind(('', server_port))
		# Listen for incoming connections
		server_socket.listen(1)
		print ('The Raspberry pi server is ready to receive')

		while True:
			data = bytes("", "utf-8")
			# Block here until a connection is accepted
			connection_socket, address = server_socket.accept()

			while True:
				new_data = connection_socket.recv(4096).decode()

				if new_data == "image": # Request for a new image
					camera.capture("new_image.jpg")

					with open("new_image.jpg", 'rb') as file:
						print("Sending new image")
						connection_socket.sendall(file.read())
						connection_socket.close()
					break # from while-loop

				if new_data == "sunlight": # Request for the sunlight report
					with open ("24h_info.txt", 'rb+') as file:
						print("Sending sunlight data")
						connection_socket.sendall(file.read())
						connection_socket.close()
						file.seek(0)
						file.truncate()
					break # from while-loop

				if new_data[:6] == "config": # Incoming config file
					conf_data = new_data[6:]
					with open("conf.txt",'w+') as file: # save to file
						file.write(conf_data)
					break # from while-loop

				if new_data[:8] == "tomatoes": # Incoming tomato data
					tomato_data = new_data[8:]
					with open("tomato.txt",'w+') as file: # save to file
						file.write(tomato_data)
					break # from while-loop


if __name__ == "__main__":
	main()

