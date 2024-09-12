import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *

# Global timer variables
timer_start_ticks = 0  
timer_limit = 25  # Limit in seconds

def display_timer(screen):
    # Calculate elapsed time
    elapsed_time = (pygame.time.get_ticks() - timer_start_ticks) / 1000  # Convert ms to seconds

    # Render timer text
    timer_text = f"Time: {int(elapsed_time)}"
    font = pygame.font.Font(None, 36)  # Font size
    timer_surface = font.render(timer_text, True, (255, 255, 255))  # White text

    # Position text in top right corner
    text_rect = timer_surface.get_rect(topright=(SCREEN_WIDTH - 20, 20))  # Adjust based on screen size
    screen.blit(timer_surface, text_rect)

def show_start_screen(screen):
    font = pygame.font.SysFont(None, 36) 
    message = (
        "You are now a lost Asteroid Miner who couldn't follow their GPS in an Asteroid Field.",
        "Survive for 25 seconds.        Rebel Scum!",
        "You trusted your technology and will now die because of it!",
        "Push the spacebar to begin"
    )

    screen.fill('black')  # Fill the screen with black background

    y_offset = SCREEN_HEIGHT / 2 - 50  # Text in middle of screen
    for line in message:
        text = font.render(line, True, 'white')
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, y_offset))
        screen.blit(text, text_rect)
        y_offset += 40  # Adjust y position for the next line

    pygame.display.flip()  

    # Wait for spacebar press
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False  # Exit loop when spacebar is pressed

def main():
    global timer_start_ticks 

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
    
    show_start_screen(screen)
    
    timer_start_ticks = pygame.time.get_ticks()

    while not game_over:
        # Calculate elapsed time
        elapsed_time = (pygame.time.get_ticks() - timer_start_ticks) / 1000

        if elapsed_time >= timer_limit:
            game_over = True  # End game after 25 seconds
            print("Time's up! You survived the asteroid field!")

        for item in updatable:
            item.update(dt)
        for asteroid in asteroids:
            if asteroid.collision(player):
                print("You got hit. Try again.") 
                game_over = True  # This ends the game.
            for shot in shots:
                if asteroid.collision(shot):
                    asteroid.split()

        dt = clock.tick()/10000
        screen.fill('black')
        
        # Draw all game objects
        for item in drawable:
            item.draw(screen)

        # Display the timer in the top right corner
        display_timer(screen)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        clock.tick(60)
    
    if game_over:
        pygame.time.wait(2000)  # Wait 2 seconds before restarting
        main()  # Restart the game

if __name__ == "__main__":
    main()
