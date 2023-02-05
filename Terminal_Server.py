# Chat Room Server side

import socket, threading

HOST_IP = socket.gethostbyname(socket.gethostname()) # Define the IP Address of the server.
HOST_PORT = 12345 # Define the number of port to be used.
ENCODER = "utf-8" # Define the Encoder to encode and decode the message.
BYTESIZE = 12345 # Define the size of message that allow to accept.

# Create a socket server with IPV4 Address and port with using TCP protocol
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()
print(f"The server ({HOST_IP}) is running...")

# Store name and socket in lists
name_list = []
socket_list = []

# define function for broadcast messages that allow to sent a message to all clients
def broadcast_message(message):
    # Send messsage to all clients that are connecting
    for client_socket in socket_list:
        client_socket.send(message)

# define function for recieve messages that recieve all of messages from any clients
def recieve_message(client_socket):
    while True:
        try:
            # Find the index of client
            inx = socket_list.index(client_socket)
            name = name_list[inx]

            # Receive message from client and pass to broadcast function
            message = client_socket.recv(BYTESIZE).decode(ENCODER)
            if message == "cd quit":
                client_socket.send("cd quit".encode(ENCODER))
                client_socket.close()
               
            message = f"\033[1;96m\t{name}: {message}\033[0m".encode(ENCODER)
            broadcast_message(message)
            
            
            
                
        except:
            # Find the index of client and remove from the lists
            inx = socket_list.index(client_socket)
            name = name_list[inx]
            socket_list.remove(client_socket)
            name_list.remove(name)

            # Close the client socket
            client_socket.close()
            message = f"\033[1;91m{name} has left the chat!\033[0m".encode(ENCODER)
            broadcast_message(message)
            break

# define function for connecting of clients that allow clients connect the server and get some information from client
def connect_client():
    while True:
        # Accept all connecting from client
        client_socket, client_address = server_socket.accept() 
        print(f"\nConnected with {client_address}...")

        # Send a order to get some information from clients
        client_socket.send("NAME".encode(ENCODER))
        client_name = client_socket.recv(BYTESIZE).decode(ENCODER)

        # Store client's information in the lists
        name_list.append(client_name)
        socket_list.append(client_socket)

        # Display the connecting client and information
        print(f"\nName of new client is {client_name}")
        client_socket.send("\nYou have connected to the server!\n".encode(ENCODER))
        broadcast_message(f"\033[1;92m{client_name} has joined the chat!\033[0m".encode(ENCODER))

        # Create threading of receive function
        recieve_thread = threading.Thread(target=recieve_message, args=(client_socket,))
        recieve_thread.start()

connect_client()       




