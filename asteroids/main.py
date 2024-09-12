import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *

# Timer variables
timer_start_ticks = 0  # We'll initialise this in the game
timer_limit = 25  # Time limit of 25 seconds

def display_timer(screen):
    # Calculate the time passed in seconds
    elapsed_time = (pygame.time.get_ticks() - timer_start_ticks) / 1000  # Convert ms to seconds

    # If elapsed time exceeds the limit, stop at 25
    if elapsed_time >= timer_limit:
        elapsed_time = timer_limit

    # Render the timer text
    timer_text = f"Time: {int(elapsed_time)}"
    font = pygame.font.Font(None, 36)  # You can adjust the font size
    timer_surface = font.render(timer_text, True, (255, 255, 255))  # White text

    # Position the text in the top right corner
    text_rect = timer_surface.get_rect(topright=(SCREEN_WIDTH - 20, 20))  # Adjust based on screen size

    # Draw the timer on the screen
    screen.blit(timer_surface, text_rect)

def show_start_screen(screen):
    font = pygame.font.SysFont(None, 36)  # Set the font and size
    message = (
        "You are now a lost Asteroid Miner who couldn't follow their GPS in an Asteroid Field.",
        "Survive for 25 seconds.        Rebel Scum!",
        "You trusted your technology and will now die because of it!",
        "Push the spacebar to begin"
    )

    screen.fill('black')  # Fill the screen with black background

    # Render and display each line of the message
    y_offset = SCREEN_HEIGHT / 2 - 50  # Start the text near the middle of the screen
    for line in message:
        text = font.render(line, True, 'white')
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, y_offset))
        screen.blit(text, text_rect)
        y_offset += 40  # Adjust y position for the next line

    pygame.display.flip()  # Update the display

    # Wait for the spacebar press
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False  # Exit the loop when spacebar is pressed

def main():
    global timer_start_ticks  # Use the global variable for the timer
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

    # Show the start screen with the introductory message
    show_start_screen(screen)

    # Start the timer once the game starts
    timer_start_ticks = pygame.time.get_ticks()  # Capture the start time

    while True:
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
        
        # Display the timer
        display_timer(screen)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        clock.tick(60)

if __name__ == "__main__":
    main()
