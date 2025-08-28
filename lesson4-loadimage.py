import pygame
import sys

pygame.init()

# 1) Create a window (screen)
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship")

# 2) Load / scale image
# Make sure you have a "spaceship.png" file in the same directory as this script
# ship_rect is used for positioning the image
ship_image = pygame.image.load("spaceship.png").convert_alpha()
ship_width, ship_height = 121 // 2, 241 // 2
ship_image = pygame.transform.scale(ship_image, (ship_width, ship_height))
ship_rect = ship_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

clock = pygame.time.Clock()

# --- MAIN GAME LOOP ---
running = True
while running:
    # A) Handle events
    # Event handling method 1 - for single key presses / releases
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.K_SPACE:
            print("Space key pressed - you can shoot!")

    # Another event handling method - for continuous movements / holding keys
    keys = pygame.key.get_pressed()
    #if keys[pygame.K_LEFT]:
    #    ship_rect.x -= 5
    #if keys[pygame.K_RIGHT]:
    #    ship_rect.x += 5

    # B) Draw
    #   Clear the screen with color. Color (20, 20, 30) is a dark blue
    window.fill((20, 20, 30))
    #   draw the ship
    window.blit(ship_image, ship_rect)
    #   present the frame
    pygame.display.flip()

    # limit Frames (Times) Per Second - run this loop at most 60 times per second
    # slows down your while-loop to ~60 FPS instead of letting it run as fast as your CPU can go
    clock.tick(60)

pygame.quit()
sys.exit()
