import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 400, 300
screen = pygame.display.set_mode((width, height))

class Polygon:
    def __init__(self, sides=4, coords=(100, 100), color=(192, 20, 2, 128), size=50, angular_velocity=0.5, speed=0.5, direction=(-1, 1)):
        self.sides = sides
        self.color = color  # RGBA color (128 is the alpha for 50% transparency)
        self.size = size
        self.coords = coords
        self.x = self.coords[0]
        self.y = self.coords[1]
        self.speed = speed
        self.direction = [direction[0] * self.speed, direction[1] * self.speed]
        self.Polypoints = []
        self.angle = 0
        self.angularVelocity = angular_velocity

        # Calculate initial polygon points
        self.update_polygon_points()

    def update_polygon_points(self):
        self.Polypoints = []
        for i in range(0, self.sides):
            angle = math.radians((360 / self.sides) * i + self.angle)
            x = self.x + self.size * math.cos(angle)
            y = self.y + self.size * math.sin(angle)
            self.Polypoints.append((x, y))

    def update(self):
        # Move and rotate the polygon
        self.x += self.direction[0]
        self.y += self.direction[1]
        self.angle += self.angularVelocity  # Rotate
        self.update_polygon_points()

    def draw(self, screen):
        # Create a surface with per-pixel alpha (transparent background)
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface = surface.convert_alpha()

        # Draw the polygon on the surface
        pygame.draw.polygon(surface, self.color, self.Polypoints)

        # Blit the surface with the polygon onto the main screen
        screen.blit(surface, (0, 0))


# Main loop
polygon = Polygon(sides=6, color=(192, 20, 2, 128))  # 128 alpha for 50% transparency

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the polygon
    polygon.update()

    # Clear the screen
    screen.fill((0,100,0))  # Fill with white background

    # Draw the polygon
    polygon.draw(screen)

    # Update the display
    pygame.display.flip()
    pygame.time.delay(10)
