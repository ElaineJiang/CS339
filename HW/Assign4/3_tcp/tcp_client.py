# -*- coding: UTF-8 -*-
from socket import *
from sys import argv
import time

import sys
reload(sys)
sys.setdefaultencoding('utf8')

BUFFER_SIZE = 100

if __name__ == "__main__":
	server_addr = argv[1]
	server_port = int(argv[2])
	server = (server_addr, server_port)

	filename = argv[3]

	f = open(filename)

	send_sock = socket(AF_INET, SOCK_STREAM)
	send_sock.connect(server)

	offset = 0
	
	file = 'filename:' + filename
	start = time.time()
	print start
	send_sock.send(file)

	while True:
		filedata = f.read(BUFFER_SIZE)
		if not filedata:
			break
		send_sock.send(filedata)

	send_sock.send('')
	send_sock.send(str(start))

	send_sock.close()