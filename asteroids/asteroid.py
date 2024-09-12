import pygame
from circleshape import *
from constants import *
import random

class Asteroid(CircleShape):
  def __init__(self,x,y, radius):
    # Initialize the CircleShape part of the Player
    super().__init__(x, y, radius )
  def draw(self,screen):
    pygame.draw.circle(screen,'red',self.position, self.radius, 2)
  def split(self):
    print(self.velocity)
    if self.radius > ASTEROID_MIN_RADIUS:
      random_angle = random.uniform(20, 50)
      rotated_velocity1 = self.velocity.rotate(random_angle)
      rotated_velocity2 = self.velocity.rotate(-random_angle)
      new_radius = self.radius-ASTEROID_MIN_RADIUS
      asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
      asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
      asteroid1.velocity = rotated_velocity1
      asteroid2.velocity = rotated_velocity2
      self.kill()
    else:
      self.kill()
      return
    
    

  def update(self, dt):
    self.position += self.velocity * dt*10