import socket
import time



class dummy:
    def __init__(self,ipee = 'localhost',port = 9999):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ipee
        self.port = port
        self.addresss = (self.ip,self.port)
        self.server.connect(self.addresss)
    
    def send_key(self,key):
        self.server.sendall(key.encode('utf-8'))
        print(f"Sent key: {key}")


time.sleep(1)  # Wait for the server to start
# Send arrow key inputs as a demonstration
keys = ['UP', 'DOWN', 'LEFT', 'RIGHT']
run = True
agent1 = dummy()
key = "hello"
while run:
    agent1.send_key(key)
    time.sleep(1)  # Wait a second between each key press
