#include<iostream>
#include<cstring>
#include<sys/socket.h>
#include<netinet/in.h>
#include<unistd.h>

#define PORT 8080
#define BUFFER_SIZE 1024

int main()
{
	int server_fd ,new_socket;
	struct sockaddr_in address;
	int opt=1;
	int addrlen=sizeof(address);
	char buffer[BUFFER_SIZE]={0};
	//creating a socket
	if((server_fd =socket(AF_INET,SOCK_STREAM,0))==0)
	{
	 perror("socket failed");
	 exit(EXIT_FAILURE);
	}
	//set socket options
	if(setsockopt(server_fd,SOL_SOCKET,SO_REUSEADDR|SO_REUSEPORT,&opt,sizeof(opt))){
	perror("setsocketopt");
	close(server_fd);
	exit(EXIT_FAILURE);
	}
	//configure server address
	address.sin_family=AF_INET;
	address.sin_addr.s_addr=INADDR_ANY;
	address.sin_port=htons(PORT);
	//bind socket to the port
	if(bind(server_fd,(struct sockaddr*)&address,sizeof(address))>0){
	perror("bind failed");
	close(server_fd);
	exit(EXIT_FAILURE);
	}
	//listen for connections
	if(listen(server_fd,3)< 0)
	{
		perror("listen failed");
		close(server_fd);
		exit(EXIT_FAILURE);
	}
	std::cout<<"server listening on port"<<PORT<<std::endl;
	//accept the client connection
	if((new_socket=accept(server_fd,(struct sockaddr*)&address,(socklen_t*)&addrlen))<0)
	{
		perror("accept failed");
		close(server_fd);
                exit(EXIT_FAILURE);
	}
	//Recieve data sand send data
	read(new_socket,buffer,BUFFER_SIZE);
	std::cout<<"message from client : "<<buffer<<std::endl;
	const char* respone ="Hello from server!";
	send(new_socket,respone,strlen(respone),0);
	std::cout<<"Response sent to client"<<std::endl;


	//close the connection
	close(new_socket);
	close(server_fd);

	return 0;

}
