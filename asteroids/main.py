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
  game_over = False # This variable switches to true when game ends and false again to restart the game

  dt = 0
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
  asteroidField = AsteroidField()

  while not game_over:
    for item in updatable:
      item.update(dt)
    for asteroid in asteroids:
      if asteroid.collision(player):
        print("You got hit. Try again.") 
        game_over = True # This ends the game.
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
    
  if game_over:
    pygame.time.wait(2000) # Wait 2 seconds before restarting
    main() # Restart the game

if __name__ == "__main__":
  main()
