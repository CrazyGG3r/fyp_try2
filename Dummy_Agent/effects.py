import pygame
import math
import random as r
from toools import diffuser
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Hexagon Drawing")
font = ["Dummy_Agent\\assets\\Fonts\\f1.ttf"]

class Polygon:
    def __init__(self,sides = 4,coords = (100,100),color = (192,20,2),size =50,angular_velocity = 0.5 , speed = 0.5,direction = (-1,1)):
        self.sides = sides
        self.color = color
        self.size  = size
        self.coords = coords
        self.x  = self.coords[0]
        self.y = self.coords[1]
        self.speed = speed
        self.direction = [direction[0]*self.speed,direction[1]*self.speed]
        self.Polypoints = []
        self.angle = 0 
        self.angularVelocity  = angular_velocity
        
        for i in range(0,self.sides):
            angle = math.radians((360/self.sides) * i)
            x = self.x + self.size * math.cos(angle)
            y = self.y + self.size * math.sin(angle)
            self.Polypoints.append((x, y))
            
    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.Polypoints)
    
    def clockwise(self):
        if self.angularVelocity < 0:
            self.angularVelocity * -1
    def anti_clockwise(self):
        if self.angularVelocity > 0:
            self.angularVelocity * -1
        
    def rotate(self,screen):
        self.Polypoints = []
        self.angle += self.angularVelocity  
        for i in range(0, self.sides):
            angle = math.radians((360 / self.sides) * i + self.angle)
            x = self.x + self.size * math.cos(angle)
            y = self.y + self.size * math.sin(angle)
            self.Polypoints.append((x, y))
    def change_color(self,color):
        self.color = color
        
    def transform(self,screen):
        self.Polypoints = []
        self.angle += self.angularVelocity  
        if self.x >= screen.get_width() - self.size:
            self.direction[0] *= -1
        if self.y >= screen.get_height() - self.size:
            self.direction[1] *= -1
        if self.x <= 0 + self.size:
            self.direction[0] *= -1
        if self.y <= 0 + self.size:
            self.direction[1] *= -1
        self.x += self.direction[0]
        self.y += self.direction[1]
        for i in range(0, self.sides):
            angle = math.radians((360 / self.sides) * i + self.angle)
            x = self.x + self.size * math.cos(angle)
            y = self.y + self.size * math.sin(angle)
            self.Polypoints.append((x, y))
class Background:
    def __init__(self,amount = 100,direction = (1,0.5,-0.5,-1),sides = 9,theme = ((0,0,0),(192,20,2))):
        self.amount    = amount
        self.direction = direction
        self.sides     = sides
        self.polygons  = []
        self.theme = theme
        self.color_list = diffuser(self.theme[0],self.theme[1])
        for a in range(amount):
            c = (r.randint(0,1280),r.randint(0,720))
            dirr = (r.choice(self.direction),r.choice(self.direction))
            temp = Polygon(sides=self.sides,coords = c,direction =dirr,color= self.color_list[r.randint(0,len(self.color_list)-1)] )
            self.polygons.append(temp)
        
    def draw(self,screen):
        for a in self.polygons:
            a.transform(screen)
            a.draw(screen)
class Text:
    def __init__(self, coords, font_size, color, text = "Hello ", fonts=0,color2 = (0,0,0),):
        self.text = text
        self.font_size = font_size
        self.color = color
        self.color2 = color2
        self.x = coords[0]
        self.y = coords[1]
        self.font = pygame.font.Font(font[fonts], font_size)
        self.color_list = diffuser(self.color,self.color2)
        self.surface = self.font.render(text, True, self.color_list[1])
        
    def update_text(self, new_text):
        self.text = new_text
        self.surface = self.font.render(new_text, True, self.color_list[1])
        
    def update_coords(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        
    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))
    
    def updateColor(self):
        self.changecolor(self.color_list[12])

    def changecolor(self, color):
        self.surface = self.font.render(self.text, True, color)
        
bg = Background(amount=250)
clock = pygame.time.Clock()
running = True

testtest = Text((400,100),120,(1,1,1),"The Brain")
while running:
    clock.tick(60)
    screen.fill((1,1,1))
    
    bg.draw(screen)
    testtest.draw(screen)
    pygame.display.flip()
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()