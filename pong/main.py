import pygame
import configs
import assets
import os
import subprocess  # To run the Asteroid game

from objects.circle import Circle
from objects.ball import Ball
from objects.block import Block

pygame.init()

screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
game_active = False  
round_won = False  
start_time = 0
game_time = 0
tap_count = 0
previous_game_time = 0
previous_tap_count = 0

assets.load_sprites()

sprites = pygame.sprite.LayeredUpdates()

circle = Circle(sprites)
block = Block(sprites)
ball = Ball(sprites)

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

def reset_game():
    global game_active, start_time, game_time, tap_count, previous_game_time, previous_tap_count, round_won
    ball.reset_position()
    previous_game_time = game_time
    previous_tap_count = tap_count
    game_time = 0
    tap_count = 0
    game_active = False  # Require spacebar to be tapped again
    round_won = False  # Reset the round won state

def draw_text(screen, text, position, font):
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect.topleft)

def check_collision(ball, block):
    global tap_count
    if pygame.sprite.collide_mask(ball, block):
        tap_count += 1

def start_asteroid_game():
    # Step 1: Move up one directory (cd ..)
    os.chdir("..")
    
    # Step 2: Change to the asteroids folder (cd .\asteroids\)
    os.chdir("./asteroids")
    
    # Step 3: Run the asteroid game (python main.py)
    subprocess.run(["python", "main.py"])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_active and not round_won:  # Start a new game
                    game_active = True
                    start_time = pygame.time.get_ticks()
                elif round_won:  # Reset for the next round or start the asteroid game
                    start_asteroid_game()  # Load Asteroid game
                    running = False  # Stop Pong game

    screen.fill("red")
    
    # Draw sprites
    sprites.draw(screen)
    
    if game_active:
        sprites.update()
        game_time = (pygame.time.get_ticks() - start_time) // 1000
        check_collision(ball, block)
        
        # Display the current tap count
        draw_text(screen, f"Taps: {tap_count}/10", (configs.SCREEN_WIDTH // 2, 50), font)

        if tap_count >= 10:  # Player has won the round
            game_active = False
            round_won = True
        
        if ball.is_outside_circle():
            reset_game()
        ball.check_collision(sprites)
    
    elif round_won:
        very_small_font = pygame.font.Font(None, 20)  
        draw_text(screen, "Well done!", (configs.SCREEN_WIDTH // 2, configs.SCREEN_HEIGHT // 2 + 80), small_font)  # Use small_font for "Well done!"
        
        draw_text(screen, "You beat this round.", (configs.SCREEN_WIDTH // 2, configs.SCREEN_HEIGHT // 2 + 100), very_small_font)
        draw_text(screen, "Press the spacebar to begin the next round", (configs.SCREEN_WIDTH // 2, configs.SCREEN_HEIGHT // 2 + 130), very_small_font)

    else:
        # Display text above circle when game hasn't started
        circle_rect = circle.rect
        draw_text(screen, "Tap spacebar to begin", (circle_rect.centerx, circle_rect.top - 50), font)
        draw_text(screen, "Hit the paddle 10x", (circle_rect.centerx, circle_rect.top - 20), small_font)
        draw_text(screen, "to progress to the next level", (circle_rect.centerx, circle_rect.top - 5), small_font)  # Reduced the gap
        draw_text(screen, f"Previous round time: {previous_game_time} seconds", (circle_rect.centerx, circle_rect.bottom + 20), small_font)
        draw_text(screen, f"Previous round taps: {previous_tap_count}", (circle_rect.centerx, circle_rect.bottom + 50), small_font)

    pygame.display.flip()
    clock.tick(configs.FPS)

pygame.quit()