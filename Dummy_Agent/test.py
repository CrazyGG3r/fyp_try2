import socket

# Connect to the Godot server
host = "127.0.0.1"  
port = 9999

# Create the socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))  # Connect to the server

# Send an action to the server (e.g., move forward)
while True:
    action = "FORWARD"
    client_socket.send(action.encode())  # Send the action as bytes



# Close the socket after sending the message
client_socket.close()
