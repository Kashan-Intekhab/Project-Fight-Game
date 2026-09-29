import sys
import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Fighting Game")

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

player_x = 200
player_y = 400
player_width = 50
player_height = 100
player_rect = pygame.Rect(player_x,player_y,player_width,player_height)
player_speed = 5
vel_y = 0          # Vertical velocity (speed going up/down)
GRAVITY = 0.8      # Pulls the player down every frame
JUMP_STRENGTH = -15 # Upward impulse when jumping (negative is UP in Pygame)
is_jumping = False # Tracks if player is currently in the air

# Main Game Loop
running = True
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] == True:
        player_rect.x -= player_speed
    if keys[pygame.K_d] == True:
        player_rect.x += player_speed
    if player_rect.left < 0:
        player_rect.left = 0
    if player_rect.right > SCREEN_WIDTH:
        player_rect.right = SCREEN_WIDTH
    if keys[pygame.K_w] and is_jumping == False:
        vel_y = JUMP_STRENGTH
        is_jumping = True
    vel_y +=  GRAVITY
    player_rect.y += vel_y
    if player_rect.y >= 400:
        player_rect.y = 400
        vel_y = 0
        is_jumping = False

    # 2. Update Display
    screen.fill((30, 30, 30))  # Dark gray background
    pygame.draw.rect(screen, (255, 0, 0), player_rect)
    pygame.display.flip()

    # 3. Cap Frame Rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()