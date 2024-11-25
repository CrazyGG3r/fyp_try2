import pygame
import math
import random as r
from toools import diffuser
pygame.init()
font = ["Dummy_Agent\\assets\\Fonts\\f1.ttf"]
def dummy(param1 = None,param2 = None):
    print("you clicked something here")
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
        self.flag = 0
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
        if self.flag  == 0:
            self.angle += self.angularVelocity  
        else:
            self.angle -= self.angularVelocity
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
    def __init__(self,amount = 100,direction = (1,0.5,-0.5,-1),sides = 9,theme = ((0,0,0),(192,20,2)),speed = 0.5,size = 50,color_limit = 1,angular_velocity = 0.5 ):
        self.amount    = amount
        self.direction = direction
        self.sides     = sides
        self.polygons  = []
        self.theme = theme
        self.color_list = diffuser(self.theme[0],self.theme[1])
        self.color_limit = color_limit
        self.speed = speed
        self.size  = size
        self.angular_velocity = angular_velocity
        for a in range(amount):
            c = (r.randint(0,1280),r.randint(0,720))
            dirr = (r.choice(self.direction),r.choice(self.direction))
            temp = Polygon(sides=self.sides,coords = c,direction =dirr,color= self.color_list[r.randint(0,len(self.color_list)-self.color_limit)],speed = self.speed ,size = self.size,angular_velocity=self.angular_velocity)
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
    
    def updateColor(self,color):
        self.changecolor(color)

    def changecolor(self, color):
        self.surface = self.font.render(self.text, True, color)
class button:
    def __init__(self, coords, size, colorInactive, colorActive, textObj,sides = 6,func = dummy,val = None,offsetx = 1.3,offsety = 4):
        self.coords = coords
        self.x = coords[0]
        self.y = coords[1]
        self.width = size - 10
        self.height = size - 10
        self.pad_x = self.x - (size/offsetx)
        self.pad_y = self.y - (size/offsety)
        self.size = size
        self.Inactivecolor = colorInactive
        self.Activecolor = colorActive
        self.text = textObj
        self.text.update_coords((self.pad_x,self.pad_y))
        self.shape = Polygon(sides,self.coords,self.Inactivecolor,self.size,speed=0)#button doesnt need to move xd
        self.action = func
        #flags
        self.value = val
        self.isClicked = False
        self.hover = False
    def draw(self, screen):
        if self.hover == True:
            self.shape.angularVelocity = 4
            self.shape.change_color(self.Activecolor)
            self.text.updateColor(self.Inactivecolor)
        else: 
            self.shape.angularVelocity = 0.5
            self.shape.change_color(self.Inactivecolor)
            self.text.updateColor(self.Activecolor)
           
        self.shape.rotate(screen)
        self.shape.draw(screen)
        self.text.draw(screen)
        
    
        
        

