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
p2_x = 700
p2_y = 400
p2_width = 50
p2_height = 100
p2_rect = pygame.Rect(p2_x, p2_y, p2_width, p2_height)
p2_speed = 5
p2_vel_y = 0
p2_is_jumping = False
font = pygame.font.SysFont(None, 24)

# Player Health
MAX_HEALTH = 100
p1_health = MAX_HEALTH
p2_health = MAX_HEALTH

# Health Bar Dimensions
HEALTH_BAR_WIDTH = 300
HEALTH_BAR_HEIGHT = 25
p1_attack_cooldown = 0
p2_attack_cooldown = 0

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

    if keys[pygame.K_LEFT] == True:
        p2_rect.x -= p2_speed
    if keys[pygame.K_RIGHT] == True:
        p2_rect.x += p2_speed
    if p2_rect.left < 0:
        p2_rect.left = 0
    if p2_rect.right > SCREEN_WIDTH:
        p2_rect.right = SCREEN_WIDTH
    if keys[pygame.K_UP] and p2_is_jumping == False:
        p2_vel_y = JUMP_STRENGTH
        p2_is_jumping = True
    p2_vel_y +=  GRAVITY
    p2_rect.y += p2_vel_y
    if p2_rect.y >= 400:
        p2_rect.y = 400
        p2_vel_y = 0
        p2_is_jumping = False
    
    # 2. Update Display
    screen.fill((30, 30, 30))  # Dark gray background

    # Draw Rectangles
    pygame.draw.rect(screen, (255, 0, 0), player_rect)
    pygame.draw.rect(screen, (0, 0, 255), p2_rect)
    
    # Draw text labels on top
    p1_text = font.render("Kashan Intekhab", True, (255, 255, 255))
    p2_text = font.render("Ali Hammad", True, (255, 255, 255))

    screen.blit(p1_text, (player_rect.x - 20, player_rect.y - 25))
    screen.blit(p2_text, (p2_rect.x - 10, p2_rect.y - 25))

    # --- Draw Health Bars ---
    # Background (Red - represents missing health)
    pygame.draw.rect(screen, (255, 0, 0), (30, 20, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
    pygame.draw.rect(screen, (255, 0, 0), (SCREEN_WIDTH - 330, 20, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))

    # Foreground (Green - represents remaining health)
    p1_health_width = int((p1_health / MAX_HEALTH) * HEALTH_BAR_WIDTH)
    p2_health_width = int((p2_health / MAX_HEALTH) * HEALTH_BAR_WIDTH)

    if p1_health > 0:
        pygame.draw.rect(screen, (0, 255, 0), (30, 20, p1_health_width, HEALTH_BAR_HEIGHT))
    if p2_health > 0:
        pygame.draw.rect(screen, (0, 255, 0), (SCREEN_WIDTH - 330, 20, p2_health_width, HEALTH_BAR_HEIGHT))

    # Player 1 Attack (F key)
    if keys[pygame.K_f] and p1_attack_cooldown == 0:
        # Attack box extends 40px out from player_rect
        p1_attack_rect = pygame.Rect(player_rect.right, player_rect.y + 20, 40, 20)
        pygame.draw.rect(screen, (255, 255, 0), p1_attack_rect)  # Visual punch indicator (Yellow)
    
        # Check if attack box hits Player 2
        if p1_attack_rect.colliderect(p2_rect):
            p2_health -=  10
            p1_attack_cooldown = 30
    # Player 2 Attack (L key)
    if keys[pygame.K_l]and p2_attack_cooldown == 0:
        # Attack box extends 40px out from player_rect
        p2_attack_rect = pygame.Rect(p2_rect.left - 40, p2_rect.y + 20, 40, 20)
        pygame.draw.rect(screen, (255, 255, 0), p2_attack_rect)  # Visual punch indicator (Yellow)
    
        # Check if attack box hits Player 1
        if p2_attack_rect.colliderect(player_rect):
            p1_health -= 10
            p2_attack_cooldown = 30
    if p1_attack_cooldown > 0:
        p1_attack_cooldown  -= 1

    if p2_attack_cooldown > 0:
        p2_attack_cooldown -= 1


    # 4. Refresh Screen
    pygame.display.flip()

    # 3. Cap Frame Rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()