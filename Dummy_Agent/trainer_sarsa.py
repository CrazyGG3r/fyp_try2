import pygame
pygame.init()
from effects import * 
import socket
import random 
import ast
import json

from SARSA import PolicyGradientAgent
import numpy as np
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
    actions = {0:"FK",1:"BK",2:"LT",3:"RT",4:"L2",5:"R2",6:"00"}
    if client_socket:
        try:
            client_socket.sendall(actions[action].encode('utf-8'))
            print(f"Action sent:{actions[action]}")
        except Exception as e:
            print(f"Failed to send action: {e}")
    else:
        print("No active connection to the server.")

def receive_state(action = "None"):
    if client_socket:
        try:
            data = client_socket.recv(1024)
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

def environment(screen,bg = None):
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
    
   
    

    brain = PolicyGradientAgent(state_dim=24, action_dim=6)
    batch_size = 64
    replay_interval = 32
    save_interval = 1 #
    actions = 0
    running = True
    episode = 0
    step = 0
    log_probs = []
    rewards = []
    while running:
        screen.fill((1,1,1))
        bg.draw(screen)
        clicked_buttons = []
        
        if flag_connect:
            state_raw = receive_state()
            if not state_raw:
                continue
            
            reward = state_raw.pop()
            done = state_raw.pop()
            state = np.array(state_raw)  # Convert to numpy array

            # Select action (note: only returns action now)
            action = brain.select_action(state)

            # Send action to environment
            send_Action(action)

            # Store the reward
            print(reward)
            brain.store_reward(reward)

            # Update policy if episode is done
            if done:
                brain.update_policy()  # No parameters needed
                episode += 1

                # Save periodically
                if episode % save_interval == 0:
                    brain.save(f"Dummy_Agent/Weights/pytorch_policyGrad/brain_ep_{episode}.pth")

            step += 1
            if step % replay_interval == 0:
                print("Updating Policy")
                brain.update_policy()  # No parameters needed
                    
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