from socket import *
import sys
import threading
import os


mutualConnections = 5
bufferSize = 4096


def proxyServer(webserver, port, connection, addr, message):
    try:
        tcpSocket = socket(AF_INET, SOCK_STREAM)
        print('entrou')
        print(webserver)
        print(port)
        tcpSocket.connect((webserver, port))
        print('conectou')
        print(message)
        tcpSocket.send(message)
        print('socket criado ok')
        while 1:
            answer = tcpSocket.recv(bufferSize)

            if(len(answer) > 0):
                connection.send(answer)
                print('tudo alright')
            else:
                break
        tcpSocket.close()
        connection.close()
    except Exception:
        print('huehue')

def connString(connection, message, addr):
    try:
        url = str(message).split('\n')[0].split(' ')[1]
        print('####################')
        print(url)
        noHttpUrl = url.find("://") # prevents http/https/whatever
        print(noHttpUrl)
        print('####################')
        if(noHttpUrl == -1):
            temp = url
            print('a')
            print(temp)
        else:
            temp = url[(noHttpUrl+3):]
            print('b')
            print(temp)
        
        portPos = temp.find(":")
        webserverPos = temp.find("/")

        if(webserverPos == -1):
            webserverPos = len(temp)
            print(webserverPos)
            print('c')
        webserver = ''
        port = -1
        print('d')
        if(portPos == -1 or webserverPos < portPos):
            port = 80
            webserver = temp[:webserverPos]
            print('e')
        else:
            port = int((temp[(portPos+1):])[:webserverPos-portPos-1])
            webserver = temp[:portPos]
            print('f')
        print('g')
        print(webserver)
        
        proxyServer(webserver, port, connection, addr, message)
        
    except Exception:
        print('hue')



def main():
    try:
        # Create a server socket, bind it to a port and start listening
        tcpSerSock = socket(AF_INET, SOCK_STREAM)
        tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)    # Use the address port even it is blocked(root requires)
        tcpSerSock.bind((sys.argv[1], 8888))
        tcpSerSock.listen(mutualConnections)
    except Exception: 
        print("Can't start server!")
        sys.exit(2)

    while 1:
        try:
            # Strat receiving data from the client
            print('Ready to serve...')
            connection, addr = tcpSerSock.accept()
            print('Received a connection from:', addr)
            message = connection.recv(bufferSize)
            #print(message)
            threading._start_new_thread(connString, (connection, message, addr))
        except Exception:
            print("Something's wrong! Closing server in 1...")
            tcpSerSock.close()
            sys.exit(1)
    
    tcpSerSock.close()



if __name__ == "__main__":

    if(len(sys.argv) == 2):
        try:
            main()
        except KeyboardInterrupt: 
            print("\nUser interruption!")
            sys.exit(2)
    else:
        print('Usage : "python3 proxy.py server_ip"\nserver_ip : It is the IP Address Of Proxy Server')
        sys.exit(2)
