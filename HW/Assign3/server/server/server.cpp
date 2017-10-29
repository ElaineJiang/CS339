/*
server: allocate a socket, respond to the client
*/

#include <windows.h>
#include <winsock.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys\stat.h>
#include <io.h>
#include <conio.h>
#include <stdlib.h>

#pragma comment(lib, "ws2_32.lib")

#define MAX 100
#define QLEN 6		//size of request queue
#define PORT 2680
#define FILE_NAME_MAX_SIZE 512
#define BUFFER_SIZE 1024


int main(int argc, char * argv[]){
	struct sockaddr_in servaddr;	//hold server address
	struct sockaddr_in clntaddr;	//hold client address
	int sockfd, addrlen, sockfd2;
	int visits = 0;
	char buf[MAX + 1];

	//start the winsock lib
#ifdef WIN32
	WSADATA wsaData;
	WSAStartup(0x0101, &wsaData);
#endif

	//set the servaddr value
	memset((char *)&servaddr, 0, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_port = PORT;
	servaddr.sin_addr.s_addr = INADDR_ANY;

	//create a socket
	sockfd = socket(PF_INET, SOCK_STREAM, 0);
	if (sockfd < 0){
		fprintf(stderr, "socket creation error\n");
		exit(1);
	}

	//bind servaddr to the socket
	if (bind(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) < 0){
		fprintf(stderr, "connect failed\n");
		exit(1);
	}

	//listen to the socket, waiting for client
	if (listen(sockfd, QLEN) < 0){
		fprintf(stderr, "listen failed\n");
		exit(1);
	}

	//Main server loop: accept and handle requests
	while (1){
		printf("Listening To Client...\n");

		sockaddr_in client_addr;
		int client_addr_len = sizeof(client_addr);

		SOCKET m_New_Socket = accept(sockfd, (sockaddr *)&client_addr, &client_addr_len);
		if (SOCKET_ERROR == m_New_Socket)
		{
			printf("Server Accept Failed: %d", WSAGetLastError());
			break;
		}

		char buffer[BUFFER_SIZE];
		memset(buffer, 0, BUFFER_SIZE);
		if (recv(m_New_Socket, buffer, BUFFER_SIZE, 0) < 0)
		{
			printf("Server Receive Data Failed!");
			break;
		}

		char file_name[FILE_NAME_MAX_SIZE + 1];
		memset(file_name, 0, FILE_NAME_MAX_SIZE + 1);
		strncpy_s(file_name, buffer, strlen(buffer)>FILE_NAME_MAX_SIZE ? FILE_NAME_MAX_SIZE : strlen(buffer));
		printf("%s\n", file_name);

		FILE * fp = fopen(file_name, "rb"); //windows下是"rb",表示打开一个只读的二进制文件 
		if (NULL == fp)
		{
			printf("File: %s Not Found\n", file_name);
		}
		else
		{
			memset(buffer, 0, BUFFER_SIZE);
			int length = 0;

			while ((length = fread(buffer, sizeof(char), BUFFER_SIZE, fp)) > 0)
			{
				if (send(m_New_Socket, buffer, length, 0) < 0)
				{
					printf("Send File: %s Failed\n", file_name);
					break;
				}
				memset(buffer, 0, BUFFER_SIZE);
			}

			fclose(fp);
			printf("File: %s Transfer Successful!\n", file_name);
		}
		closesocket(m_New_Socket);
	}

}