import socket
import os
from datetime import datetime

# Create a folder to save the images
if not os.path.exists('images'):
    os.makedirs('images')

# Set server parameters
HOST = '127.0.0.1'  # Local address
PORT = 9998  # Port number (you can choose any available port)

# Create Socket Server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server is listening on {HOST}:{PORT}...")
    
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            
            # To store all received data
            data = b""
            while True:
                # Receive 4096 bytes of data at a time until there is no more data
                part = conn.recv(4096)
                if not part:
                    break
                data += part
            
            # Extract image data
            # Assume the data is sent in multipart/form-data format, so we need to find the boundary
            if b'\r\n\r\n' in data:
                headers, image_data = data.split(b'\r\n\r\n', 1)
            else:
                print("Error: Invalid data received")
                continue

            # Create a filename in the format "year-month-day-hour-minute-second-microsecond"
            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
            filename = f"images/{timestamp}.jpg"

            # Save the image data
            with open(filename, 'wb') as f:
                f.write(image_data)

            print(f"Image saved as {filename}")

            # Send a response back to the client
            response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nImage received and saved"
            conn.sendall(response)