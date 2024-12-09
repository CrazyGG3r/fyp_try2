
import pygame
pygame.init()
from effects import * 
import socket
import random 
import ast
import json

from noobs import DQNAgent

client_socket = None

def connect_to_env(screen = None, Background = None, addr = 'localhost',port = 9999):
    global client_socket
    try:
        server_address = (addr, port)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)
        print("Connected to the server.")
        
        

    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def disconnect_from_server(screen= None, bg = None):
    if client_socket:
        client_socket.close()
        print("Disconnected from the server.")

def send_Action(action= "Hello"):
    if client_socket:
        try:
            client_socket.sendall(action.encode('utf-8'))
            print(f"Action sent:{action}")
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
              print("state: ",decoded_state)
              json_decoded_data = json.loads(decoded_state)
              parsed_data = [ast.literal_eval(item) for item in json_decoded_data]
              print("sttta: ",parsed_data)
              return parsed_data
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
    #-0-0-0--00-0-0-0-0-0-0-
    #=-=-=-=- Action Buttons
    text_mov_up     = Text((0,0),25,(200,28,10),"UP   ")
    text_mov_down   = Text((0,0),25,(200,28,10),"DOWN ")
    text_mov_left   = Text((0,0),25,(200,28,10),"LEFT ")
    text_mov_right  = Text((0,0),25,(200,28,10),"RIGHT")
    text_rot_right  = Text((0,0),25,(200,28,10),"20 DEG >") 
    text_rot_left   = Text((0,0),25,(200,28,10),"20 DEG <")
    text_random_but  = Text((0,0),25,(200,28,10),"Random")
    button_up       = button((screen.get_width()*1/8,300),75,c2,c1,text_mov_up   ,4,send_Action,"FK",2) 
    button_down     = button((screen.get_width()*2/8,300),75,c2,c1,text_mov_down ,4,send_Action,"BK",2)
    button_left     = button((screen.get_width()*3/8,300),75,c2,c1,text_mov_left ,4,send_Action,"LT",2)
    button_right    = button((screen.get_width()*4/8,300),75,c2,c1,text_mov_right,4,send_Action,"RT",2)
    button_rt_right = button((screen.get_width()*5/8,300),75,c2,c1,text_rot_right,4,send_Action,"R2",2)  
    button_rt_left  = button((screen.get_width()*6/8,300),75,c2,c1,text_rot_left ,4,send_Action,"L2",2)  
    button_random  = button((screen.get_width()*1/8,500),80,c2,c1,text_random_but ,4,send_Action,"RA",2)  
    all_butts = [button1,button2,button_up,button_right,button_down,button_left,button_rt_left,button_rt_right,button_random]
    command_butts = [button_up,button_right,button_down,button_left,button_rt_left,button_rt_right]
    running = True
    ##____--=-=-=-=-=-==-=- Agent declaration and stufff___#####
    brain = DQNAgent(22,6)
    
    flag_rand = 0
    flag_connect = 0
    while running:
        screen.fill((1,1,1))
        bg.draw(screen)
        clicked_buttons = []

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
        if flag_rand == 1 and client_socket:
            temp = random.choice(command_butts)
            temp.action(temp.value)
        for a in clicked_buttons:
            a.isClicked = False
            if a.text.text == "Connect":
                flag_connect == True
            if a.text.text != "Connect" or a.text.text!= "Disconnect":
                if a.value == "RA" and flag_rand == 0:
                    flag_rand = 1
                else:
                    flag_rand = 0 
                a.action(a.value)
            else:
                a.action(screen,bg)
        if flag_connect:
            receive_state()
        else:
            print("Not connected")
        pygame.display.flip()
    
   
