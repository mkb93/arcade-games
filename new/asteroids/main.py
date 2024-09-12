import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *

def main():
  print("Starting asteroids!")
  print(f'Screen width: {SCREEN_WIDTH}')
  print(f'Screen height: {SCREEN_HEIGHT}')

  pygame.init()
  clock = pygame.time.Clock()
  updatable = pygame.sprite.Group()
  drawable = pygame.sprite.Group()
  asteroids = pygame.sprite.Group()
  shots = pygame.sprite.Group()
  Player.containers = (updatable, drawable)
  Asteroid.containers = (asteroids, updatable, drawable)
  AsteroidField.containers = (updatable,)
  Shot.containers = (shots, updatable, drawable)

  dt = 0
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
  asteroidField = AsteroidField()
  while 1 == 1:
    for item in updatable:
      item.update(dt)
    for asteroid in asteroids:
      if asteroid.collision(player):
        print('Game over!')
        return
      for shot in shots:
        if asteroid.collision(shot):
          asteroid.split()

    dt = clock.tick()/10000
    screen.fill('black')
    for item in drawable:
      item.draw(screen)
    pygame.display.flip()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return
    clock.tick(60)
if __name__ == "__main__":
  main()
