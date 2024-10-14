import os
import socket
from datetime import datetime

# Create Socket Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))  # Listen on all IP addresses, port 12345
server_socket.listen(5)  # Maximum number of pending connections

print("Server started, waiting for client connections...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Client connected: {client_address}")

    # Receive data
    request_data = client_socket.recv(4096)

    # Get the current time and generate a filename
    current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"request/{current_time}.bin"
    
    os.makedirs("request", exist_ok=True)

    # Save the received data as a binary file
    with open(filename, "wb") as file:
        file.write(request_data)

    print(f"Client request data saved as: {filename}")

    # Close the client connection
    client_socket.close()
