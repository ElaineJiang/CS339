/*
Client: connect the server, upload/download files
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

#define MAX 100			//max buffer size
#define PORT 2680		//default TCP port number
#define FILE_NAME_MAX 512	//file name max size
#define BUFFER_SIZE 1024

int main(int argc, char * argv[]){
	struct sockaddr_in servaddr;	//struct to hold server's address
	int sockfd, n;		//socker descriptor
	char buf[MAX + 1];
	unsigned long temp;

	//start the winsock lib
#ifdef WIN32
	WSADATA wsaData;
	WSAStartup(0x0101, &wsaData);
#endif

	//set servaddr value
	memset((char *)&servaddr, 0, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	if (argc < 2){
		printf("usage:client<ipaddress>\n");
		system("pause");
		exit(0);
	}

	servaddr.sin_port = PORT;
	temp = inet_addr((const char FAR *) argv[1]);
	memcpy(&servaddr.sin_addr, &temp, sizeof(servaddr.sin_addr));

	//create a socket
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (sockfd < 0){
		fprintf(stderr, "socket creation error\n");
		system("pause");
		exit(1);
	}

	//connect the socket to the specified server
	if (connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) < 0){
		fprintf(stderr, "connect failed\n");
		system("pause");
		exit(1);
	}

	while (true){

		char file_name[FILE_NAME_MAX + 1];
		memset(file_name, 0, FILE_NAME_MAX + 1);
		printf("Please input filename you request on the server: ");
		scanf("%[^\n]%*c", &file_name);

		if (27 == file_name[0]){
			break;
		}

		char buffer[BUFFER_SIZE];
		memset(buffer, 0, BUFFER_SIZE);
		strncpy(buffer, file_name, strlen(file_name) > BUFFER_SIZE ? BUFFER_SIZE : strlen(file_name));

		if (send(sockfd, buffer, BUFFER_SIZE, 0) < 0){
			printf("Send file name failed\n");
			system("pause");
			exit(1);
		}

		//open the file
		FILE *fp = fopen(file_name, "wb");
		if (NULL == fp){
			printf("File %s can not be opened\n", file_name);
			system("pause");
			exit(1);
		}
		else{
			memset(buffer, 0, BUFFER_SIZE);
			int length = 0;
			while ((length = recv(sockfd, buffer, BUFFER_SIZE, 0)) > 0){
				if (fwrite(buffer, sizeof(char), length, fp) < length){
					printf("File %s write failed\n", file_name);
					break;
				}
				memset(buffer, 0, BUFFER_SIZE);
			}

			printf("Received File %s from server success \n", file_name);
		}

		fclose(fp);
		
	}

	//close the socket
	closesocket(sockfd);
	system("pause");
	exit(0);
}