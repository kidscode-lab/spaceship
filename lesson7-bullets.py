# Kids-Code Lab - Lesson 5
#   On Lesson 4:
#       Pygame Basics - Display a window
#       Pygame Basics - Setup main game loop
#       Pygame Basics - Handle events (keyboard, mouse, quit)
#       Load spaceship image and display it on the screen
#       Moving a spaceship with arrow keys
#   On Lesson 5:
#       5.1 Turn the spaceship image smoothly towards the direction of movement
#       5.2 Add background image
#       5.3 Add falling rocks (asteroids) that reset to the top when they go off the bottom of the screen
#   Lesson 6:
#       6.1 Load sound effects for collision
#       6.2 Collision detection between spaceship and rocks
#       6.3 Add background music
#   Lesson 7:
#       7.1 Build a mask for rock surface
#       7.2 Cache rotated ship images + masks to keep FPS high
#       7.3 Rotate ship via cache and keep center
#       7.4 Update collision from rectangle to mask
#       7.5 Load bullet sprite
#       7.6 A right-facing laser sprite needs this rotation to face direction
#       7.7 Setup firing bullet function
#       7.8 Fire on Space key
#       7.9 Move & cull bullets
#       7.10 Draw bullets
#       7.11 Load laser / pew sound
#       7.12 Play laser sound when bullet fires

import pygame
import sys
import os
import random
from functools import lru_cache

pygame.init()
pygame.mixer.init()

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
ship_rect = ship_image.get_rect(center=(WIDTH // 3, HEIGHT // 3))

# Lesson 5.2 - Load and scale background image
background_image = pygame.image.load('assets\\purple_background.png').convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Lesson 5.3 - Load rock images from assets sub-directory and store it to a list
rock_images = []
for i in range(1, 15):
    filename = 'assets\\' + str(i).zfill(3) + '.png'
    image = pygame.image.load(filename).convert_alpha()
    rock_images.append(image)

# Lesson 5.3 - create rocks list and populate it with random rocks
# Each rock is represented as a dictionary with its image, rectangle, and falling speed
NUM_ROCKS = 10  # number of rocks
rocks = []
for _ in range(NUM_ROCKS):
    img = random.choice(rock_images)

    rect = img.get_rect(
        center=(random.randint(0, WIDTH), random.randint(-HEIGHT, 0))
    )
    speed = random.randint(2, 6)  # random falling speed
    # Lesson 7.1 - Build a mask for rock surface
    mask = pygame.mask.from_surface(img)
    rocks.append({"img": img, "rect": rect, "speed": speed, "mask": mask})    
    # rocks.append({"img": img, "rect": rect, "speed": speed})

# Lesson 7.5 - Load bullet sprite
BULLET_PATH = os.path.join("assets", "lasers", "01.png")
BULLET_BASE = pygame.image.load(BULLET_PATH).convert_alpha()

# Lesson 6.1 - Load sound effects
collision_sound = pygame.mixer.Sound(os.path.join("assets", "explosion.wav"))
# Lesson 7.11 - Load laser / pew sound
laser_sound = pygame.mixer.Sound(os.path.join("assets", "lasers", "S04.mp3"))

# Lesson 6.3 - Load and play background music
pygame.mixer.music.load(os.path.join("assets", "background3.wav"))
pygame.mixer.music.play(-1)  # play the music in a loop

#  3) Initialize game paramters
ship_x, ship_y = WIDTH / 2, HEIGHT - 100
ship_speed = 5

#   rotation
direction = 0
#       make rotation smooth
target_direction = 0
rotation_speed = 5 

# 7.2 - Cache rotated ship images + masks to keep FPS high
ANGLE_STEP = 3

def _qa(a):  # quantize angle
    return int(round(a / ANGLE_STEP) * ANGLE_STEP) % 360

@lru_cache(maxsize=240)
def get_rotated_ship(angle_q):
    """Return (rotated_image, mask) for a quantized angle."""
    img = pygame.transform.rotate(ship_image, angle_q)
    mask = pygame.mask.from_surface(img)
    return img, mask

# 7.6 - A right-facing laser sprite needs this rotation to face direction
rotate_ccw = (direction - 270) % 360

@lru_cache(maxsize=240)
def get_rotated_bullet(angle_q):
    """Rotate the RIGHT-facing bullet to game direction 'angle_q'."""
    rotate_ccw = (angle_q - 270) % 360  # from RIGHT to target direction
    img = pygame.transform.rotozoom(BULLET_BASE, rotate_ccw, 1.0)
    mask = pygame.mask.from_surface(img)
    return img, mask

# 7.7 - Setup firing bullet function
BULLET_SPEED = 12
FIRE_COOLDOWN_MS = 160
last_shot_time = 0
bullets = []  # {"surf","mask","rect","vx","vy"}

def fire_bullet(ship_center, angle_deg, ship_rect_for_offset):
    """Spawn a bullet at the ship’s nose, moving in ship direction."""
    # movement vector (matches your angle convention)
    import math
    rad = math.radians(angle_deg)
    vx = -math.sin(rad)
    vy = -math.cos(rad)

    # rotate sprite+mask to the current direction (quantized)
    angle_q = _qa(angle_deg)
    surf, mask = get_rotated_bullet(angle_q)

    # spawn a bit in front of the ship “nose”
    nose_offset = int(max(ship_rect_for_offset.width, ship_rect_for_offset.height) * 0.55)
    bx = ship_center[0] + vx * nose_offset
    by = ship_center[1] + vy * nose_offset

    rect = surf.get_rect(center=(int(bx), int(by)))

    bullets.append({"surf": surf, "mask": mask, "rect": rect, "vx": vx, "vy": vy})
    # 7.12 Play laser sound when bullet fires
    laser_sound.play()

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
        # 7.8 Fire on Space key
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            now = pygame.time.get_ticks()
            if now - last_shot_time >= FIRE_COOLDOWN_MS:
                fire_bullet(ship_rect.center, direction, ship_rect)
                last_shot_time = now

    # Another event handling method - for continuous movements / holding keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship_rect.x -= ship_speed
        target_direction = 90
    elif keys[pygame.K_RIGHT]:
        ship_rect.x += ship_speed
        target_direction = 270
    elif keys[pygame.K_UP]:
        ship_rect.y -= ship_speed
        target_direction = 0
    elif keys[pygame.K_DOWN]:
        ship_rect.y += ship_speed
        target_direction = 180

    # Lesson 5.1 - update direction
    #   rotate smoothly towards target direction
    #   variable diff is the difference between target direction and current direction
    #   it is always a positive value between 0 and 360
    #   if diff > 180, it means we need to rotate counter-clockwise
    #   if diff < 180, it means we need to rotate clockwise
    diff = (target_direction - direction) % 360
    if diff != 0:
        if diff > 180:
            direction -= rotation_speed
        else:
            direction += rotation_speed
        direction %= 360    # keep direction between 0-359
        # prevent overshooting
        if abs((target_direction - direction) % 360) < rotation_speed:
            direction = target_direction

    #   Lesson 5.3 - Update rock positions
    for rock in rocks:
        rock["rect"].y += rock["speed"]
        if rock["rect"].top > HEIGHT:
            # reset rock to the top with a new random x position and speed
            rock["rect"].center = (random.randint(0, WIDTH), random.randint(-HEIGHT, 0))
            rock["speed"] = random.randint(2, 6)

    # 7.4 - Update collision from rectangle to mask
    #     - remark section 6.2
    # 6.2 - Collision detection between spaceship and rocks
    # for rock in rocks:
    #     if ship_rect.colliderect(rock["rect"]):
    #         collision_sound.play()
    #         # reset rock to the top with a new random x position and speed
    #         # rock["rect"].center = (random.randint(0, WIDTH), random.randint(-HEIGHT, 0))
    #         # rock["speed"] = random.randint(2, 6)
    #         pygame.time.delay(500)  # pause for half a second to let the sound play
    #         running = False  # end the game on collision

    # 7.3 - Rotate ship via cache and keep center
    angle_q = _qa(direction)
    old_center = ship_rect.center
    rotated_ship_img, ship_mask = get_rotated_ship(angle_q)
    ship_rect = rotated_ship_img.get_rect(center=old_center)

    # 7.4 - Update collision from rectangle to mask
    hit = False
    for rock in rocks:
        if not ship_rect.colliderect(rock["rect"]):
            continue
        # Offset from ship to rock for mask alignment
        offset = (rock["rect"].left - ship_rect.left, rock["rect"].top - ship_rect.top)
        if ship_mask.overlap(rock["mask"], offset):
            hit = True
            break

    if hit:
        collision_sound.play()
        pygame.time.delay(500)
        running = False

    # 7.9 Move & cull bullets
    alive_bullets = []
    for b in bullets:
        b["rect"].x += int(b["vx"] * BULLET_SPEED)
        b["rect"].y += int(b["vy"] * BULLET_SPEED)
        if -50 <= b["rect"].right and b["rect"].left <= WIDTH + 50 and -50 <= b["rect"].bottom and b["rect"].top <= HEIGHT + 50:
            alive_bullets.append(b)
    bullets = alive_bullets

    new_bullets = []
    for b in bullets:
        hit_any = False
        for rock in rocks:
            if not b["rect"].colliderect(rock["rect"]):
                continue
            offset = (rock["rect"].left - b["rect"].left, rock["rect"].top - b["rect"].top)
            if b["mask"].overlap(rock["mask"], offset):
                # respawn rock
                rock["rect"].center = (random.randint(0, WIDTH), random.randint(-HEIGHT, 0))
                rock["speed"] = random.randint(2, 6)
                collision_sound.play()
                hit_any = True
                break
        if not hit_any:
            new_bullets.append(b)
    bullets = new_bullets

    # B) Draw
    #   Clear the screen with color - (20, 20, 30) is a dark blue
    #   if background_image is loaded, draw it instead of filling with color
    # window.fill((20, 20, 30))

    #   Lesson 5.2 - draw the background
    window.blit(background_image, (0, 0))

    #   Lesson 5.1 - draw the ship
    #       Remark this line and uncomment the next 4 lines to see the difference
    # window.blit(ship_image, ship_rect)

    # 7.4 - remark below block
    #   Lesson 5.1 - draw the ship rotated to the current direction
    # rotated_ship_img = pygame.transform.rotate(ship_image, direction)
    # ship_rect = rotated_ship_img.get_rect(center=ship_rect.center)
    # rotated_ship_img.get_rect(center=ship_rect.center)
    window.blit(rotated_ship_img, ship_rect)

    #   Losson 5.3 - draw rocks
    for rock in rocks:
        window.blit(rock["img"], rock["rect"])

    # 7.10 Draw bullets
    for b in bullets:
        window.blit(b["surf"], b["rect"])

    #   Present the frame
    pygame.display.flip()

    #   limit Frames (Times) Per Second - run this loop at most 60 times per second
    #   slows down your while-loop to ~60 FPS instead of letting it run as fast as your CPU can go
    clock.tick(60)
# --- END OF GAME LOOP ---

# 5) Clean up
pygame.quit()
sys.exit()
