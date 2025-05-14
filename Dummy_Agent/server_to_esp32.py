import socket

HOST = '0.0.0.0'
PORT = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Server started. Waiting for ESP32 to connect...")
conn, addr = server.accept()
print(f"ESP32 connected from {addr}")

while True:
    cmd = input("Enter command to send to ESP32: ")
    conn.sendall((cmd + "\n").encode())

    if cmd.upper() == "EXIT":
        break

    data = b""
    while not data.endswith(b"\n"):
        chunk = conn.recv(1024)
        if not chunk:
            break
        data += chunk

    response = data.decode().strip()
    print(f"ESP32: {response}")
