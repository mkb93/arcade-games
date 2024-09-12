import pygame
from circleshape import *
from constants import *
from shot import *

class Player(CircleShape):
  def __init__(self,x,y, rotation = 0):
    # Initialize the CircleShape part of the Player
    super().__init__(x, y, PLAYER_RADIUS )
    self.rotation = rotation
    self.shot_cooldown = 0.0


  def triangle(self):
    forward = pygame.Vector2(0, 1).rotate(self.rotation)
    right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
    a = self.position + forward * self.radius
    b = self.position - forward * self.radius - right
    c = self.position - forward * self.radius + right
    return [a, b, c]
    
  def draw(self, screen):
    pygame.draw.polygon(screen, 'white', self.triangle(), 2)
  
  def rotate(self, dt):
    self.rotation += PLAYER_TURN_SPEED*dt* 10
  
  def move(self, dt):
    forward = pygame.Vector2(0, 1).rotate(self.rotation)
    self.position += forward * PLAYER_SPEED * dt *10

  def shoot(self):
    self.shot_cooldown = PLAYER_SHOT_COOLDOWN
    shot = Shot(self.position.x, self.position.y)
    direction = pygame.Vector2(0, 1).rotate(self.rotation)
    shot.velocity += direction * PLAYER_SHOT_SPEED

  def update(self, dt):
    self.shot_cooldown -= dt*100
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
      self.move(dt)
    if keys[pygame.K_s]:
      self.move(-dt)
    if keys[pygame.K_a]:
      self.rotate(-dt)
    if keys[pygame.K_d]:
      self.rotate(dt)
    if keys[pygame.K_SPACE] and self.shot_cooldown <= 0:
      self.shoot()