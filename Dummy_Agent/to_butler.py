import pygame
pygame.init()
from effects import * 
import socket
import random 
import ast
import json


def dummy():
    print("hello")
    pass





def to_butler(screen,bg = None):
    c1 = (20,1,1)
    c2 = (195,25,2)
    bg = Background(10,sides=9,speed = 0.01,size = 220,color_limit= 20,angular_velocity= 0.01)
    
    #=-=-=-- Connect | Disconnect buttons
    butt1 = Text((0,0),30,(192,20,2),"  Connect")
    button1 = button((screen.get_width()/8,100),90,c2,c1,butt1,8,dummy)
    butt2 = Text((0,0),30,(192,20,2),"Disconnect",)
    button2 = button((screen.get_width()*7/8,100),90,c2,c1,butt2,8,dummy)

    all_butts = [button1,button2]
    running = True
    
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
        pygame.display.flip()
