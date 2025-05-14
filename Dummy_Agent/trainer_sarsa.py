import pygame
pygame.init()
from effects import * 
import socket
import random 
import re
import time

client_socket = None
flag_connect = False
last_state = None  # Store the last received state

def connect_to_env(screen=None, Background=None, addr='localhost', port=9999):
    global client_socket
    global flag_connect
    try:
        server_address = (addr, port)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)
        print("Connected to the server.")
        flag_connect = True
        # Send an initial hello to establish connection
        send_Action("HELLO")
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

def disconnect_from_server(screen=None, bg=None):
    global client_socket
    global flag_connect
    if client_socket:
        client_socket.close()
        client_socket = None
        flag_connect = False
        print("Disconnected from the server.")

def send_Action(action="Hello"):
    if client_socket:
        try:
            client_socket.sendall((action + '\n').encode('utf-8'))
            print(f"Action sent: {action}")
            # Add a small delay to ensure messages don't overlap
            time.sleep(0.1)
        except Exception as e:
            print(f"Failed to send action: {e}")
    else:
        print("No active connection to the server.")

def parse_state_array(data_str):
    """
    Parse the state vector from the raw string format:
    [x,y,z,...][a,b,c,...][...] into a list of state vectors
    """
    # Extract arrays using regex to find content between square brackets
    array_matches = re.findall(r'\[(.*?)\]', data_str)
    
    if not array_matches:
        print("No arrays found in data")
        return None
    
    state_vectors = []
    for match in array_matches:
        try:
            # Split by comma and convert to float
            values = [float(x.strip()) for x in match.split(',')]
            if len(values) == 40:  # Ensure we have exactly 40 elements
                state_vectors.append(values)
            else:
                print(f"Warning: Expected 40 values but got {len(values)}")
        except ValueError as e:
            print(f"Error parsing values: {e}")
    
    return state_vectors

def receive_state():
    global client_socket, last_state
    if not client_socket:
        print("Cannot receive state: No active connection")
        return None
        
    try:
        # Set a timeout to avoid blocking forever
        client_socket.settimeout(0.5)
        data = b''
        part = client_socket.recv(4096)
        if part:
            data += part
            # Continue receiving if more data available
            while len(part) == 4096:
                part = client_socket.recv(4096)
                if not part: break
                data += part
        
                
        if data:
            decoded_state = data.decode("utf-8").strip()
            print(f"Raw state received (first 100 chars): {decoded_state}...")
            
            try:
                # Try our custom parser for the array format
                state_vectors = parse_state_array(decoded_state)
                if state_vectors and len(state_vectors) > 0:
                    print(f"Successfully parsed {len(state_vectors)} state vectors")
                    # Just use the most recent state vector
                    last_state = state_vectors[-1]
                    return last_state
                else:
                    print("Failed to parse any valid state vectors")
                    return last_state
            except Exception as e:
                print(f"Parse error: {e}")
                return last_state
        else:
            print("Empty data received")
            return last_state
    except Exception as e:
        print(f"Error receiving data: {e}")
        # If we get a connection error, reset the connection
        if isinstance(e, ConnectionError):
            disconnect_from_server()
        return last_state

def environment(screen, bg=None):
    global flag_connect, last_state
    c1 = (20,1,1)
    c2 = (195,25,2)
    bg = Background(10, sides=9, speed=0.01, size=220, color_limit=20, angular_velocity=0.01)
    
    # Create a font for displaying state values
    state_font = pygame.font.SysFont("Arial", 16)
    
    #=-=-=-- Connect | Disconnect buttons
    butt1 = Text((0,0), 30, (192,20,2), "  Connect")
    button1 = button((screen.get_width()/8, 100), 90, c2, c1, butt1, 8, connect_to_env)
    
    butt2 = Text((0,0), 30, (192,20,2), "Disconnect")
    button2 = button((screen.get_width()*7/8, 100), 90, c2, c1, butt2, 8, disconnect_from_server)
    
    #=-=-=-=- Action Buttons
    text_mov_up     = Text((0,0), 25, (200,28,10), "UP   ")
    text_mov_down   = Text((0,0), 25, (200,28,10), "DOWN ")
    text_mov_left   = Text((0,0), 25, (200,28,10), "LEFT ")
    text_mov_right  = Text((0,0), 25, (200,28,10), "RIGHT")
    text_rot_right  = Text((0,0), 25, (200,28,10), "20 DEG >") 
    text_rot_left   = Text((0,0), 25, (200,28,10), "20 DEG <")
    text_random_but = Text((0,0), 25, (200,28,10), "Random")
    text_get_state  = Text((0,0), 25, (200,28,10), "Get State")
    
    button_up       = button((screen.get_width()*1/8, 300), 75, c2, c1, text_mov_up, 4, send_Action, "FD", 2) 
    button_down     = button((screen.get_width()*2/8, 300), 75, c2, c1, text_mov_down, 4, send_Action, "BD", 2)
    button_left     = button((screen.get_width()*3/8, 300), 75, c2, c1, text_mov_left, 4, send_Action, "LT", 2)
    button_right    = button((screen.get_width()*4/8, 300), 75, c2, c1, text_mov_right, 4, send_Action, "RT", 2)
    button_rt_right = button((screen.get_width()*5/8, 300), 75, c2, c1, text_rot_right, 4, send_Action, "R2", 2)  
    button_rt_left  = button((screen.get_width()*6/8, 300), 75, c2, c1, text_rot_left, 4, send_Action, "L2", 2)  
    button_random   = button((screen.get_width()*1/8, 500), 80, c2, c1, text_random_but, 4, send_Action, "RA", 2)
    button_get_state = button((screen.get_width()*3/8, 500), 80, c2, c1, text_get_state, 4, receive_state, None, 2)
    
    all_butts = [button1, button2, button_up, button_right, button_down, button_left, 
                button_rt_left, button_rt_right, button_random, button_get_state]
    command_butts = [button_up, button_right, button_down, button_left, button_rt_left, button_rt_right]
    
    running = True
    flag_rand = 0
    
    # Status text
    status_font = pygame.font.SysFont("Arial", 24)
    
    # Create a clock object to control frame rate
    clock = pygame.time.Clock()
    fps = 30
    
    last_state_check = time.time()
    state_check_interval = 0.5  # Check for state every 0.5 seconds
    
    while running:
        screen.fill((1,1,1))
        bg.draw(screen)
        clicked_buttons = []

        for a in all_butts:
            a.draw(screen)
            
        # Draw connection status
        status_text = f"Connection: {'Connected' if flag_connect else 'Disconnected'}"
        status_surface = status_font.render(status_text, True, (0, 255, 0) if flag_connect else (255, 0, 0))
        screen.blit(status_surface, (screen.get_width()/2 - 100, 50))
        
        # Show state values if available
        if last_state:
            y_pos = 380
            cols = 4  # Display in 4 columns
            items_per_col = 10  # 10 items per column
            
            for i, val in enumerate(last_state):
                col = i // items_per_col
                row = i % items_per_col
                
                x_pos = 50 + col * 180
                y_offset = row * 20
                
                label = f"State[{i}]: {val:.2f}"
                value_text = state_font.render(label, True, (200, 200, 200))
                screen.blit(value_text, (x_pos, y_pos + y_offset))

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
                a.shape.flag = 0
                
        # Handle random movement if enabled
        if flag_rand == 1 and flag_connect:
            temp = random.choice(command_butts)
            temp.action(temp.value)
            
        # Process clicked buttons
        for a in clicked_buttons:
            a.isClicked = False
            if a.text.text not in ["Connect", "Disconnect"]:
                if a.value == "RA":
                    flag_rand = 1 if flag_rand == 0 else 0
                elif a.text.text == "Get State":
                    # Explicitly request state
                    a.action()
                else:
                    a.action(a.value)
            else:
                a.action(screen, bg)
                
        # Regularly check for state updates if connected
        current_time = time.time()
        if flag_connect and (current_time - last_state_check) > state_check_interval:
            receive_state()
            last_state_check = current_time
            
        pygame.display.flip()
        clock.tick(fps)
    
    # Ensure clean disconnect when exiting
    disconnect_from_server()