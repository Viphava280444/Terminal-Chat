
# Chat Room client side

import socket, threading, sys

DEST_PORT = 12345 # Define the number of port to be used.
ENCODER = "utf-8" # Define the Encoder to encode and decode the message.
BYTESIZE = 12345 # Define the size of message that allow to accept.
status = True
# Create a socket client with IPV4 Address and port with using TCP protocol



# define function for sending messages that allow to sent a message to all clients
def send_message():
    global status
    while True:
        message = input("")
        client_socket.send(message.encode(ENCODER))
        if message == "cd quit":
            client_socket.close()
        if status == False:
            break    
      

# define function for recieve messages that recieve all of messages from any clients
def recieve_message():
    global status
    while True:
        try:
            message = client_socket.recv(BYTESIZE).decode(ENCODER)

            # Check it is order or simple message
            if message == "NAME":
                name = input("\nEnter your name: ")
                client_socket.send(name.encode(ENCODER))    
            elif message == "cd quit":
                client_socket.close()
                status = False
                break       
            else:
                print(message)   

        except:
            print("\nAn error has occured...")
            client_socket.close()
            break                 
    connection()

# Check status of the server of the IP Address
def connection():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        ip_input = input("Type the IP Address to join the server\n>>> ")
        dest_ip = ip_input
        try:
            client_socket.connect((dest_ip, DEST_PORT))
            break
        except:
            print()
            print("The server of this IP Address is not running.")    
            print()
    global status 
    status = True

    recieve_threading = threading.Thread(target=recieve_message)
    send_threading = threading.Thread(target=send_message)

    recieve_threading.start()
    send_threading.start() 

        

        
connection()


        
