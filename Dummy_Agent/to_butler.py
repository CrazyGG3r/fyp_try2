import pygame
pygame.init()
from effects import * 
import socket
import random 
import ast
import json
from noobs_cpu import Agent
import numpy as np
import os
client_socket = None
flag_connect = False
def connect_to_env(screen = None, Background = None, addr = 'localhost',port = 9999):
    global client_socket
    global flag_connect
    try:
        server_address = (addr, port)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)
        print("Connected to the server.")
        flag_connect = True
    except Exception as e:
        print(f"Connection failed: {e}")
        return None 

def disconnect_from_server(screen= None, bg = None):
    if client_socket:
        client_socket.close()
        print("Disconnected from the server.")

def send_Action(action= 0):
    actions = {0:"FK",1:"BK",2:"L2",3:"R2",4:"00"}
    if client_socket:
        try:
            print("About to send action:",action)
            client_socket.sendall(actions[action].encode('utf-8'))
            print(f"Action sent:{actions[action]}")
        except Exception as e:
            print(f"Failed to send action: {e}")
    else:
        print("No active connection to the server.")

def receive_state(action = "None"):
    if client_socket:
        try:
            print("Waiting to receive data")
            data = client_socket.recv(1024)
            print("Data received: ",data)
            if data:
                decoded_state = data.decode("utf-8")
                # print("state: ", decoded_state)
                # Directly parse the JSON data
                json_decoded_data = json.loads(decoded_state)
                # print("state: ", json_decoded_data)
                
                return json_decoded_data
        except Exception as e:
            print(f"Error receiving data: {e}")
state = None

def to_butler(screen,bg = None):
    c1 = (20,1,1)
    c2 = (195,25,2)
    bg = Background(10,sides=9,speed = 0.01,size = 220,color_limit= 20,angular_velocity= 0.01)
    
    #=-=-=-- Connect | Disconnect buttons
    butt1 = Text((0,0),30,(192,20,2),"  Connect")
    button1 = button((screen.get_width()/8,100),90,c2,c1,butt1,8,connect_to_env)
    butt2 = Text((0,0),30,(192,20,2),"Disconnect",)
    button2 = button((screen.get_width()*7/8,100),90,c2,c1,butt2,8,disconnect_from_server)
    butt3 = Text((0,0),30,(192,20,2),"Start Training",)
    button3 = button((screen.get_width()*4/8,100),110,c2,c1,butt3,8)
    all_butts = [button1,button2,button3]
    
    #-0-0-0--00-0-0-0-0-0-0- DQN AGENT
    brain = Agent(38, 5)
    last_episode = 481  # Use the same episode number you trained with
    brain.load(f"Dummy_Agent/weights_2.0/brain_ep_{last_episode}.weights.h5")

    # Disable exploration for testing
    brain.epsilon = 0  # Always use the learned policy
    brain.epsilon_min = 0
    
   
    
    while True:
        screen.fill((1,1,1))
        bg.draw(screen)
        clicked_buttons = []
        if flag_connect:
            
            state_raw = receive_state()
            if state_raw is None:
                continue
                
            # Remove reward and done flags (not needed for testing)
            _ = state_raw.pop()  # reward
            _ = state_raw.pop()  # done
            
            state = np.reshape(state_raw, (1, len(state_raw)))
            
            # Get action from policy (no random exploration)
            action = brain.act(state)
            print("Current state:", state_raw, "Selected action:", action)
            
            # Send action to environment
            send_Action(action)
                
        for a in all_butts:
            a.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                    for a in all_butts:
                        if a.hover:
                            if not a.isClicked:
                                a.isClicked = True
                                clicked_buttons.append(a)
                        if event.type == pygame.MOUSEBUTTONUP:
                            for a in all_butts:
                                if a.hover:
                                    a.isClicked = False
        m = pygame.mouse.get_pos()
        for a in all_butts:
            if m[0] > a.x - a.width and m[1] > a.y - a.height:
                if m[0] < (a.x + a.width) and m[1] < (a.y + a.height):
                    a.hover = True
                    a.shape.flag = 1
                else:
                    a.hover = False
                    a.shape.flag = 0
            else:
                a.hover = False
        for a in clicked_buttons:
            a.isClicked = False
            if a.text.text != "Connect" or a.text.text!= "Disconnect":
                if a.value == "RA" and flag_rand == 0:
                    flag_rand = 1
                else:
                    flag_rand = 0 
                a.action(a.value)
            else:
                a.action(screen,bg)
        pygame.display.flip()