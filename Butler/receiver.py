import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt(zmq.SUBSCRIBE, b'')

def receive_data():
    while True:
        data = socket.recv_json()
        print("Received data:", data)
        # Process or forward data as needed

receive_data()
#BUTLER
#HEXAPOD
#AI AGENT
#BUTLER

#ai agent - 1 device

#hexapod - 1 device

#butler server - 1 device

def receive_action():
    pass#ai agent se action receive

def send_state_vector():
    pass#ai agent ko statevector send

def send_action():
    pass#hexapod ko action send

def receive_state_vector():
    pass#state_vector

