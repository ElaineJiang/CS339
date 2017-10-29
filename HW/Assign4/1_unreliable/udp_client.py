# -*- coding: UTF-8 -*-
from socket import *
from sys import argv
import time

import sys
reload(sys)
sys.setdefaultencoding('utf8')

SEGMENT_SIZE = 100

if __name__ == "__main__":
	server_addr = argv[1]
	server_port = int(argv[2])
	server = (server_addr, server_port)

	filename = argv[3]

	with open(filename) as f:
		content = f.read()

	send_sock = socket(AF_INET, SOCK_DGRAM)

	offset = 0
	
	file = 'filename:' + filename
	start = time.time()
	print start
	send_sock.sendto(file, server)

	while offset < len(content):
		if offset + SEGMENT_SIZE > len(content):
			segment = content[offset:]
		else:
			segment = content[offset:(offset + SEGMENT_SIZE)]
		offset += SEGMENT_SIZE

		send_sock.sendto(segment, server)

	send_sock.sendto('', server)
	send_sock.sendto(str(start), server)

	send_sock.close()