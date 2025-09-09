import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Demo")

# Rectangle 1: Center of the screen
rect1 = pygame.Rect(WIDTH // 2 - 25, HEIGHT // 2 - 25, 50, 50)

# Rectangle 2: Start at top-left, moves with keyboard
rect2 = pygame.Rect(100, 100, 50, 50)
speed = 5

# Font setup
# None for default font, 72 for large size
font = pygame.font.SysFont(None, 72)

start_showing = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    oldx = rect2.x
    oldy = rect2.y
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rect2.x -= speed
    if keys[pygame.K_RIGHT]:
        rect2.x += speed
    if keys[pygame.K_UP]:
        rect2.y -= speed
    if keys[pygame.K_DOWN]:
        rect2.y += speed

    # Check for collision
    if rect1.colliderect(rect2):
        collision = True
        rect2.x = oldx
        rect2.y = oldy
    else:
        collision = False

    window.fill((0, 0, 0))
    pygame.draw.rect(window, (255, 0, 0), rect1)  # Center rectangle (red)
    pygame.draw.rect(window, (0, 255, 0), rect2)  # Moving rectangle (green)

    if collision:
        text_surface = font.render("Collision", True, (255, 255, 0))
        text_rect = text_surface.get_rect(topright=(WIDTH-20, 20))
        window.blit(text_surface, text_rect)
    
    pygame.display.flip()
    pygame.time.delay(20)

pygame.quit()
sys.exit()