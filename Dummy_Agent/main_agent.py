import pygame
pygame.init()

from effects import *


screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Hexagon Drawing")
bg = Background(amount=200)
clock = pygame.time.Clock()
running = True

heading = Text((400,100),120,(10,1,1),"The Brain")
textscreen = [heading]

#buttons
c1 = (20,1,1)
c2 = (195,25,2)
instructions = Text((0,0),30,(192,20,2),"Instructions")
button1= button((screen.get_width()/6,200),90,c1,c2,instructions,8)
txtt = Text((0,0),70,(192,20,2),"Connect")
button2 = button((screen.get_width()/2,button1.y+ 200),140,(20,1,1),(195,25,5),txtt,7)
creditss = Text((0,0),30,(192,20,2)," Credits")
button3 = button(((screen.get_width()/6)*5,200),60,c1,c2,creditss,8)
Start_train = Text((0,0),25,(192,20,2)," Start Trainig")
all_butts = [button1,button2,button3]
while running:
    clock.tick(60)
    screen.fill((1,1,1))
    clicked_buttons = []
    
    bg.draw(screen)
    
    for a in textscreen:
        a.draw(screen)
    for a in all_butts:
        a.draw(screen)
        
    pygame.display.flip()
  
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
        print("cock")

    

pygame.quit()
