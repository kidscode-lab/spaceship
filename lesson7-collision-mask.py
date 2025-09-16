import pygame
import sys
import os
from functools import lru_cache

pygame.init()

# --- Window ---
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Image Collision Demo — Mask")

# --- Paths ---
SHIP_PATH = os.path.join("assets", "spaceship.png")
ROCK_PATH = os.path.join("assets", "001.png")

# --- Colors & Fonts ---
BG   = (18, 20, 28)
FG   = (235, 235, 235)
YELL = (255, 220, 0)
GREEN= (100, 235, 140)
GREY = (140, 140, 140)

FONT_BIG = pygame.font.SysFont(None, 48)
FONT     = pygame.font.SysFont(None, 26)

def label(text, pos, color=FG):
    screen.blit(FONT.render(text, True, color), pos)

def load_image_fit(path, max_w=260, max_h=260):
    img = pygame.image.load(path).convert_alpha()
    w, h = img.get_width(), img.get_height()
    scale = min(1.0, max_w / w, max_h / h)
    if scale < 1.0:
        img = pygame.transform.smoothscale(img, (int(w*scale), int(h*scale)))
    return img

# --- Load assets ---
try:
    ship_base = load_image_fit(SHIP_PATH, 260, 260)
    rock_img  = load_image_fit(ROCK_PATH, 220, 220)
except Exception as e:
    print(f"Failed to load images from assets/: {e}")
    pygame.quit(); sys.exit(1)

# Positions/rects
ship_rect = ship_base.get_rect(center=(WIDTH//2, HEIGHT//2))
rock_rect = rock_img.get_rect(topleft=(120, 120))

# Static rock mask
rock_mask = pygame.mask.from_surface(rock_img)

# Ship rotation cache (image + mask per angle)
ANGLE_STEP = 3
def q(a): return int(round(a / ANGLE_STEP) * ANGLE_STEP) % 360

@lru_cache(maxsize=240)
def get_rotated_ship(angle_q):
    img = pygame.transform.rotate(ship_base, angle_q)
    mask = pygame.mask.from_surface(img)
    return img, mask

ship_angle = 0
ship_img, ship_mask = get_rotated_ship(q(ship_angle))

speed = 6
clock = pygame.time.Clock()

# UI toggles
show_overlap_point = True      # show the first overlapped pixel as a yellow dot
show_image_outlines = False    # optional: draw thin rects around images (visual aid)

running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    # Move rock with arrows
    if keys[pygame.K_LEFT]:  rock_rect.x -= speed
    if keys[pygame.K_RIGHT]: rock_rect.x += speed
    if keys[pygame.K_UP]:    rock_rect.y -= speed
    if keys[pygame.K_DOWN]:  rock_rect.y += speed

    # Rotate ship with Q/E
    turn = 0
    if keys[pygame.K_q]: turn -= 3
    if keys[pygame.K_e]: turn += 3
    if turn:
        ship_angle = (ship_angle + turn) % 360
        angle_q = q(ship_angle)
        old_center = ship_rect.center
        ship_img, ship_mask = get_rotated_ship(angle_q)
        ship_rect = ship_img.get_rect(center=old_center)

    # Reset rock position
    if keys[pygame.K_r]:
        rock_rect.topleft = (120, 120)

    # Toggle visuals
    if keys[pygame.K_o]: show_overlap_point = True
    if keys[pygame.K_p]: show_overlap_point = False
    if keys[pygame.K_1]: show_image_outlines = not show_image_outlines

    # --- MASK-ONLY COLLISION ---
    mask_hit = False
    overlap_point = None
    if ship_rect.colliderect(rock_rect):  # cheap broad-phase (still mask-only result)
        offset = (rock_rect.left - ship_rect.left, rock_rect.top - ship_rect.top)
        overlap_point = ship_mask.overlap(rock_mask, offset)  # (x, y) or None
        mask_hit = overlap_point is not None

    # --- Draw ---
    screen.fill(BG)
    screen.blit(ship_img, ship_rect)
    screen.blit(rock_img, rock_rect)

    # Optional outlines of the images (not circle/rect tests—just visual boxes)
    if show_image_outlines:
        pygame.draw.rect(screen, GREY, ship_rect, 1)
        pygame.draw.rect(screen, GREY, rock_rect, 1)

    # Show first overlapping pixel
    if mask_hit and show_overlap_point:
        px = ship_rect.left + overlap_point[0]
        py = ship_rect.top + overlap_point[1]
        pygame.draw.circle(screen, YELL, (px, py), 4)

    # UI text
    title = FONT_BIG.render("Mask (Pixel-Perfect) Collision — Only", True, FG)
    screen.blit(title, title.get_rect(center=(WIDTH//2, 30)))
    label(f"Mask overlap: {'HIT' if mask_hit else 'no'}", (20, 90), GREEN if mask_hit else GREY)
    label("Arrows: move rock   Q/E: rotate ship   R: reset   ESC: quit", (20, HEIGHT - 60))
    label("O/P: show/hide overlap dot   1: toggle image outlines", (20, HEIGHT - 34))

    pygame.display.flip()

pygame.quit()
sys.exit()
