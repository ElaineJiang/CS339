# -*- coding: UTF-8 -*-
from socket import *
from sys import argv, stdout
import re
import time

import sys
reload(sys)
sys.setdefaultencoding('utf8')

BUFFER_SIZE = 100

if __name__ == "__main__":
	server_addr = argv[1]
	server_port = int(argv[2])
	server = (server_addr, server_port)

	recv_sock = socket(AF_INET, SOCK_STREAM)
	recv_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	recv_sock.bind(server)
	recv_sock.listen(True)
	print 'Waiting for connecting to port:', server_port

	sock, addr = recv_sock.accept()
	print "Connected."

	while True:
		try:
			content = sock.recv(BUFFER_SIZE)
			if re.match(r'filename:.+', content):
				filename = content[9:]
				fp = open(filename,'wb')
				continue
			if re.match(r'\d+\.\d+', content):
				start = float(content)
				try:
					delta = end - start
					print 'delta', delta
					break
				except:
					continue

			if content == '':
				end = time.time()
				print end
				fp.close()
				print 'file', filename,'received'
				break
			else:
				fp.write(content)
		except (KeyboardInterrupt, SystemExit):		
			break
	sock.close()