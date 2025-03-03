import socket

HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 9999 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"Server started on {HOST}:{PORT}, waiting for ESP32...")

conn, addr = server.accept()
print(f"ESP32 Connected from {addr}")

while True:
    command = input("Enter command: ").strip()
    if command.lower() == "exit":
        break

    conn.sendall((command + "\n").encode())  # Send command
    print("Sent:", command)

conn.close()
server.close()
print("Server closed.")
