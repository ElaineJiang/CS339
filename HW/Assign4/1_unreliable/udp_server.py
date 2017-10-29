# -*- coding: UTF-8 -*-
from socket import *
from sys import argv, stdout
import re
import time

import sys
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":
	server_addr = argv[1]
	server_port = int(argv[2])
	server = (server_addr, server_port)

	recv_sock = socket(AF_INET, SOCK_DGRAM)
	recv_sock.bind(server)

	print 'Listening on port:', server_port

	while True:
		try:
			content, address = recv_sock.recvfrom(4096)
			if re.match(r'filename:.+', content):
				filename = content[9:]
				fp = open(filename,'wb')
				continue
			if re.match(r'\d+\.\d+', content):
				start = float(content)
				try:
					delta = end - start
					print 'delta', delta
					continue
				except:
					continue

			if content == '':
				end = time.time()
				print end
				fp.close()
				print 'file', filename,'received'
			else:
				fp.write(content)

		except (KeyboardInterrupt,SystemExit):
			break
	recv_sock.close()