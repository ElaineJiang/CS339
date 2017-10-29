# -*- coding: UTF-8 -*-
from socket import *
from sys import argv

import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')

SEGMENT_SIZE = 100

def ip_checksum(data):
	pos = len(data)
	if (pos & 1):  # If odd...
		pos -= 1
		sum = ord(data[pos])  # Prime the sum with the odd end byte
	else:
		sum = 0

    #Main code: loop to calculate the checksum
	while pos > 0:
		pos -= 2
		sum += (ord(data[pos + 1]) << 8) + ord(data[pos])

	sum = (sum >> 16) + (sum & 0xffff)
	sum += (sum >> 16)

	result = (~ sum) & 0xffff  # Keep lower 16 bits
	result = result >> 8 | ((result & 0xff) << 8)  # Swap bytes
	return chr(result / 256) + chr(result % 256)



def rdt_file(server_addr, server_port, filename):
	# server_addr = argv[1]
	server_port = int(server_port)
	server = (server_addr, server_port)
	listen_addr = server_addr
	listen_port = server_port + 1
	listen = (listen_addr, listen_port)#listen to ACK
	# filename = argv[3]
	with open(filename) as f:
		content = f.read()

	file = 'filename:' + filename

	send_sock = socket(AF_INET, SOCK_DGRAM)
	recv_sock = socket(AF_INET, SOCK_DGRAM)

	recv_sock.bind(listen)
	recv_sock.settimeout(1)

	offset = 0
	seq = 0
	
	start = time.time() 				#start timer
	print start
	send_sock.sendto(file, server)		#send filename, first bit

	while offset < len(content):
		if offset + SEGMENT_SIZE > len(content):
			segment = content[offset:]
		else:
			segment = content[offset:(offset + SEGMENT_SIZE)]
		offset += SEGMENT_SIZE

		ack_received = False

		while not ack_received:
			segment = ip_checksum(segment) + str(seq) + segment
			#encode the checksum and seq #
			send_sock.sendto(segment, server)

			try:
				msg, address = recv_sock.recvfrom(4096)
			except timeout:
				print "Timeout"
			else:
				print msg
				checksum = msg[:2]
				ack_seq = msg[5]
				if ip_checksum(msg[2:]) == checksum and ack_seq == str(seq):
					ack_received = True

		seq = 1 - seq

	send_sock.sendto('', server)
	send_sock.sendto(str(start), server)

	print "File", filename, "sent."

	send_sock.close()
	recv_sock.close()
	return

def main():
	while True:
		info = raw_input("Please input the address, port num and filename you want to transfer in sequence separated by space:\n")
		info_list = info.split()
		server_addr = info_list[0]
		server_port = info_list[1]
		filename = info_list[2]
		rdt_file(server_addr, server_port, filename)
		resume = raw_input("Continue to transfer?(y/n)")
		if resume == 'n':
			return



if __name__ == "__main__":
	main()
