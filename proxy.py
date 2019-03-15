from socket import *
import sys
import threading
import os


mutualConnections = 5
bufferSize = 4096


def proxyServer(webserver, port, connection, addr, message):
    try:
        tcpSocket = socket(AF_INET, SOCK_STREAM)
        tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)    # Use the address port even it is blocked(root requires)
        tcpSocket.connect((webserver, port))
        print("proxy <==> client connection started.")
        tcpSocket.send(message)

        while 1:
            answer = tcpSocket.recv(bufferSize)

            if(len(answer) > 0):
                connection.send(answer)
                print("Answer sent!")
            else:
                break
            
        tcpSocket.close()
        connection.close()
        print("proxy <==> client connection ended.")
    except Exception:
        print()
        print("Something do wrong while sending message from proxy to browser!")
        print("The port must be blocked, try to run as root if you aren't.\n")

def connString(connection, message, addr):
    try:
        print("####\nTo connection: {}".format(addr))
        url = str(message).split('\n')[0].split(' ')[1]
        print("## url: {}".format(url))
        noHttpUrl = url.find("://") # prevents http/https/whatever, but no duplicated urls/strange urls

        if(noHttpUrl == -1):
            temp = url
        else:
            temp = url[(noHttpUrl+3):]
        
        portPos = temp.find(":")
        webserverPos = temp.find("/")

        if(webserverPos == -1):
            webserverPos = len(temp)

        webserver = ''
        port = -1

        if(portPos == -1 or webserverPos < portPos):
            port = 80
            webserver = temp[:webserverPos]
        else:
            port = int((temp[(portPos+1):])[:webserverPos-portPos-1])
            webserver = temp[:portPos]

        print("## webserver: {}".format(webserver))
        print("####\n")
        
        proxyServer(webserver, port, connection, addr, message)
        
    except Exception:
        print()
        print("Something do wrong in message manipulation!\n")



def main():
    try:
        # Create a server socket, bind it to a port and start listening
        tcpSerSock = socket(AF_INET, SOCK_STREAM)
        tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)    # Use the address port even it is blocked(root requires)
        tcpSerSock.bind((sys.argv[1], 8888))
        tcpSerSock.listen(mutualConnections)
    except Exception: 
        print()
        print("Can't start server!")
        print("The port must be blocked, try to run as root if you aren't.\n")
        sys.exit(2)

    while 1:
        try:
            # Strat receiving data from the client
            print('Ready to serve...\n')
            connection, addr = tcpSerSock.accept()
            print('Received a connection from:', addr)
            message = connection.recv(bufferSize)
            print("Starting a new thread...\n")
            threading._start_new_thread(connString, (connection, message, addr))
        except Exception:
            print()
            print("Something's wrong! Closing server in 1...\n")
            tcpSerSock.close()
            sys.exit(1)
    
    tcpSerSock.close()



if __name__ == "__main__":

    if(len(sys.argv) == 2):
        try:
            main()
        except KeyboardInterrupt: 
            print()
            print("\nUser interruption!zn")
            sys.exit(2)
    else:
        print()
        print('Usage : "python3 proxy.py server_ip"')
        print("server_ip : It is the IP Address Of Proxy Server\n")
        sys.exit(2)
