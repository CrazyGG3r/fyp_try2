import pygame
import math
import random as r

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Hexagon Drawing")

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
        pygame.draw.polygon(screen,self.color, self.Polypoints)
    
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

amount = 500
pees = []
direction_choice = (1,0.5,-0.5,-1)
ss = 15
# ss = r.randint(3,10)
for a in range(amount):
    c = (r.randint(0,1280),r.randint(0,720))
    dirr = (r.choice(direction_choice),r.choice(direction_choice))
    temp = Polygon(sides=ss,coords = c,direction =dirr )
    pees.append(temp)


clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    screen.fill((1,1,1))
    
    # Draw hexagon
    for a in pees:
        a.transform(screen)
        a.draw(screen)
    
    pygame.display.flip()
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()