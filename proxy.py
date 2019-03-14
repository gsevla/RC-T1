from socket import *
import sys
import threading
import os


mutualConnections = 10
bufferSize = 2048


def connString(connection, message, addr):
    try:
        print(message.split()[1])
        filename = str(message.split()[1]).partition("/")[2]
        print(filename)
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
            print("Something's wrong! Closing server in 2...")
            tcpSerSock.close()
            sys.exit(2)
    
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
