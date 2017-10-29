# -*- coding: UTF-8 -*-
from socket import *
from sys import argv
import os
import re
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def send(sock, content, addr):
	checksum = ip_checksum(content)
	sock.sendto((checksum+content), addr)

def ip_checksum(data):
	pos = len(data)
	if (pos & 1):
		pos -= 1
		sum = ord(data[pos])
	else:
		sum = 0
	while pos > 0:
		pos -= 2
		sum += (ord(data[pos + 1]) << 8) + ord(data[pos])

	sum = (sum >> 16) + (sum & 0xffff)
	sum += (sum >> 16)

	result = (~ sum) & 0xffff
	result = result >> 8 | ((result & 0xff) << 8)
	return chr(result / 256) + chr(result % 256)



def main():
	listen_addr = argv[1]
	listen_port = int(argv[2])
	listen = (listen_addr, listen_port)
	ack_addr = argv[1]
	ack_port = int(listen_port) + 1	#port to send ACK_seq
	ack = (ack_addr, ack_port)

	ack_sock = socket(AF_INET, SOCK_DGRAM)
	recv_sock = socket(AF_INET, SOCK_DGRAM)
	recv_sock.bind(listen)

	print "Listening on port:", listen_port

	expecting_seq = 0

	while True:
		try:
			message, address = recv_sock.recvfrom(4096)

			if re.match(r'filename:.+', message):
				filename = message[9:]
				fp = open(filename,'wb')
				continue
			if re.match(r'\d+\.\d+', message):
				start = float(message)
				try:
					delta = end - start
					print 'delta', delta
					continue
				except:
					continue
			if message == '':
				end = time.time()
				print end
				fp.close()
				print 'file', filename, 'received'
				continue


			checksum = message[:2]
			seq = message[2]
			content = message[3:]

			if ip_checksum(content) == checksum:
				send(ack_sock, "ACK" + seq, ack)
				if seq == str(expecting_seq):
					fp.write(content)
					expecting_seq = 1 - expecting_seq
			else:
				negative_seq = str(1-expecting_seq)
				send(ack_sock, "ACK" + negative_seq, ack)
		except (KeyboardInterrupt, SystemExit):
			break
	ack_sock.close()
	recv_sock.close()

if __name__ == "__main__":
	main()
