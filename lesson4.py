# Kids-Code Lab - Lesson 4
#   Pygame Basics - Display a window
#   Pygame Basics - Setup main game loop
#   Pygame Basics - Handle events (keyboard, mouse, quit)
#   Load spaceship image and display it on the screen
#   Moving a spaceship with arrow keys
#   Turn the spaceship image smoothly towards the direction of movement
#   Add falling rocks (asteroids) that reset to the top when they go off the bottom of the screen

import pygame
import sys
import os

pygame.init()

# 1) Create a window (screen)
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship")

# 2) Load Game Assets
# Make sure you have a "spaceship.png" file in the same directory as this script 
#   or on "assets" sub-directory 
# Loadd spaceship image from assets sub-directory
ship_image = pygame.image.load(os.path.join("assets", "spaceship.png")).convert_alpha()
ship_width, ship_height = ship_image.get_width() // 2, ship_image.get_height() // 2
# Scale the image to half its original size
ship_image = pygame.transform.scale(ship_image, (ship_width, ship_height))
# Create a rectangle for positioning using the scaled size of spacehip image
ship_rect = ship_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# 3) Initialize game paramters
ship_x, ship_y = WIDTH / 2, HEIGHT - 100
ship_speed = 5

#   Setup game clock - used to control frame rate (FPS)
clock = pygame.time.Clock()

# 4) --- MAIN GAME LOOP ---
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
    if keys[pygame.K_LEFT]:
        ship_rect.x -= ship_speed
    elif keys[pygame.K_RIGHT]:
        ship_rect.x += ship_speed
    elif keys[pygame.K_UP]:
        ship_rect.y -= ship_speed
    elif keys[pygame.K_DOWN]:
        ship_rect.y += ship_speed

    # B) Draw
    #   Clear the screen with color - (20, 20, 30) is a dark blue
    window.fill((20, 20, 30))
    #   draw the ship
    window.blit(ship_image, ship_rect)
    #   present the frame
    pygame.display.flip()

    # limit Frames (Times) Per Second - run this loop at most 60 times per second
    # slows down your while-loop to ~60 FPS instead of letting it run as fast as your CPU can go
    clock.tick(60)
# --- END OF GAME LOOP ---

# 5) Clean up
pygame.quit()
sys.exit()
