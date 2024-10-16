import socket
import time

def send_key(key):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 9999))
        s.sendall(key.encode('utf-8'))
        print(f"Sent key: {key}")

if __name__ == "__main__":
    time.sleep(1)  # Wait for the server to start
    # Send arrow key inputs as a demonstration
    keys = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    for key in keys:
        send_key(key)
        time.sleep(1)  # Wait a second between each key press
