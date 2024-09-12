import pygame
import configs
import assets
from objects.circle import Circle
from objects.ball import Ball
from objects.block import Block

pygame.init()

screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
game_active = False  # Variable to track if the game has started
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

font = pygame.font.Font(None, 36)  # Default font and size 36 for the instruction text
small_font = pygame.font.Font(None, 24)  # Smaller font for the counters

def reset_game():
    global game_active, start_time, game_time, tap_count, previous_game_time, previous_tap_count
    ball.reset_position()
    previous_game_time = game_time
    previous_tap_count = tap_count
    game_time = 0
    tap_count = 0
    game_active = False  # Require spacebar to be tapped again

def draw_text(screen, text, position, font):
    text_surface = font.render(text, True, (255, 255, 255))  # White color text
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect.topleft)

def check_collision(ball, block):
    global tap_count
    if pygame.sprite.collide_mask(ball, block):
        tap_count += 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True  # Start the game when spacebar is pressed
                start_time = pygame.time.get_ticks()

    screen.fill("red")
    
    # Draw sprites
    sprites.draw(screen)
    
    if game_active:
        sprites.update()
        game_time = (pygame.time.get_ticks() - start_time) // 1000
        check_collision(ball, block)
        if ball.is_outside_circle():
            reset_game()
        ball.check_collision(sprites)
    else:
        # Display the text above the circle
        circle_rect = circle.rect
        draw_text(screen, "Tap spacebar to begin", (circle_rect.centerx, circle_rect.top - 50), font)
        draw_text(screen, f"Previous round time: {previous_game_time} seconds", (circle_rect.centerx, circle_rect.bottom + 20), small_font)
        draw_text(screen, f"Previous round taps: {previous_tap_count}", (circle_rect.centerx, circle_rect.bottom + 50), small_font)

    pygame.display.flip()
    clock.tick(configs.FPS)

pygame.quit()
