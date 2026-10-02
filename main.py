import sys
import pygame

# Initialize Pygame  
pygame.init()  


# Initialize Pygame Mixer
pygame.mixer.init()
# --- Background Music Setup ---
pygame.mixer.music.load("Sounds/bg_music.mp3")
pygame.mixer.music.set_volume(0.1)  # Keep volume moderate (0.0 to 1.0) so sound effects stay clear
pygame.mixer.music.play(-1)          # '-1' means loop infinitely!


# Load Sound Effects
punch_sound = pygame.mixer.Sound("Sounds/punch.ogg")
fireball_sound = pygame.mixer.Sound("Sounds/fireball.wav")
hit_sound = pygame.mixer.Sound("Sounds/hit.wav")
block_sound = pygame.mixer.Sound("Sounds/block.wav")
bump_sound = pygame.mixer.Sound("Sounds/bump.aiff")

# Set Volume Levels (0.0 to 1.0)
punch_sound.set_volume(0.9)
fireball_sound.set_volume(0.9)
hit_sound.set_volume(1.0)
block_sound.set_volume(1.0)
bump_sound.set_volume(0.2)

match_intro_timer = 120  # 2 seconds (at 60 FPS)
round_number = 1
# Shield duration limits (120 frames = 2 seconds max shield)
MAX_SHIELD_TIME = 40
p1_shield_timer = 0
p2_shield_timer = 0

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Fighting Game")

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

round_time = 60                       # 60 seconds
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 1000)   # Fires every 1000ms (1 sec)
player_x = 200
player_y = 400
player_width = 50
player_height = 100
player_rect = pygame.Rect(player_x,player_y,player_width,player_height)
p1_fireball = None       # Stores the Rect for P1's fireball
p1_fireball_speed = 10   # Moves right (+x)
p1_fireball_cd = 0       # Fireball cooldown timer

p2_fireball = None       # Stores the Rect for P2's fireball
p2_fireball_speed = -10  # Moves left (-x)
p2_fireball_cd = 0       # Fireball cooldown timer


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
large_font = pygame.font.SysFont(None, 60)
small_font = pygame.font.SysFont(None, 30)




# Player Health
MAX_HEALTH = 100
p1_health = MAX_HEALTH
p2_health = MAX_HEALTH

# Health Bar Dimensions
HEALTH_BAR_WIDTH = 300
HEALTH_BAR_HEIGHT = 25
p1_attack_cooldown = 0
p2_attack_cooldown = 0

game_over = False
winner_text = ""
p1_score = 0
p2_score = 0

# Global Particle List
particles = []

import random
def spawn_particles(x,y,color, count = 12):
    for i in range(0,count):
        particle = {'x': x,'y': y,'vel_x': random.uniform(-5, 5),
            'vel_y': random.uniform(-5, 5),   # Random vertical spread
            'life': random.randint(10, 20),     # Exists for 10-20 frames
            'color': color,
            'size': random.randint(3, 6)}
        particles.append(particle)
    

# Main Game Loop
running = True
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == TIMER_EVENT and not game_over:
            round_time -= 1

    p1_eye_rect = pygame.Rect(player_rect.right - 12, player_rect.y + 15, 8,  8)
    p2_eye_rect = pygame.Rect(p2_rect.left  + 4, p2_rect.y + 15, 8,8)
    p1_nose_rect = pygame.Rect(player_rect.right - 12, player_rect.y + 30, 30,  8)
    p2_nose_rect = pygame.Rect(p2_rect.left-17, p2_rect.y + 30, 30,  8)
    p1_hand_rect = pygame.Rect(player_rect.right-45, player_rect.y + 55, 20,15)
    p2_hand_rect = pygame.Rect(p2_rect.left + 25, p2_rect.y+55,20,15)
    grass_rect = pygame.Rect(0,500,SCREEN_WIDTH,100)

    keys = pygame.key.get_pressed()
    if p1_health <= 0 and not game_over:
        p2_score += 1
        game_over = True
        winner_text = "Ali Hammad Wins!"
        pygame.mixer.music.fadeout(1000)  # Smoothly fades music out over 1 second


    if p2_health <= 0 and not game_over:
        p1_score += 1
        game_over = True
        winner_text = "Kashan Intekhab Wins!"
        pygame.mixer.music.fadeout(1000)  # Smoothly fades music out over 1 second

    # 2. Update Display
    screen.fill((30, 30, 30))  # Dark gray background
    target_region = (0,0,1000,500)
    screen.fill((20,24,40),rect = target_region)

    # Wrap all movement, jumping, physics, and attack checks inside an IF NOT game_over: condition so player inputs are ignored when the fight is finished.
    if not game_over:
        # Match intro text
        if match_intro_timer > 60:
            round1_text = large_font.render(f"ROUND {round_number}", True, (255, 255, 255))
            screen.blit(round1_text, (SCREEN_WIDTH // 2 -60, SCREEN_HEIGHT//2 - 50))
        else:
             if match_intro_timer > 0:
                fight_text = large_font.render("FIGHT!", True, (255, 255, 255))
                screen.blit(fight_text, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT//2 - 50))
        if match_intro_timer > 0:
           match_intro_timer -= 1



        if keys[pygame.K_s] and keys[pygame.K_a]:
            p1_is_blocking = True
        if keys[pygame.K_s] and keys[pygame.K_d]:
            p1_is_blocking = True

        
        if keys[pygame.K_DOWN]  and keys[pygame.K_LEFT]:
            p2_is_blocking = True
        if keys[pygame.K_DOWN]  and keys[pygame.K_RIGHT]:
            p2_is_blocking = True
        # --- Player 1 Shield Check (S key) ---
        p1_is_blocking = False
        if keys[pygame.K_s] and not is_jumping:
            if p1_shield_timer < MAX_SHIELD_TIME:
                p1_is_blocking = True
                p1_shield_timer += 1  # Shield active, count up!
            else:
                p1_is_blocking = False  # Time expired! Shield auto-removed!
        else:
            # Recharge shield when key is released
            if p1_shield_timer > 0:
                p1_shield_timer -= 1

        # --- Player 2 Shield Check (DOWN ARROW) ---
        p2_is_blocking = False
        if keys[pygame.K_DOWN] and not p2_is_jumping:
            if p2_shield_timer < MAX_SHIELD_TIME:
                p2_is_blocking = True
                p2_shield_timer += 1  # Shield active, count up!
            else:
                p2_is_blocking = False  # Time expired! Shield auto-removed!
        else:
            # Recharge shield when key is released
            if p2_shield_timer > 0:
                p2_shield_timer -= 1
        # Draw P1 Shield Duration Bar
        if p1_is_blocking:
            shield_pct = (MAX_SHIELD_TIME - p1_shield_timer)/MAX_SHIELD_TIME
            pygame.draw.rect(screen,(0,200,255),(player_rect.x,player_rect.y - 10, int(player_width*shield_pct),5))
        # Draw P2 Shield Duration Bar
        if p2_is_blocking:
            shield_pct = (MAX_SHIELD_TIME - p2_shield_timer)/MAX_SHIELD_TIME
            pygame.draw.rect(screen,(0,200,255),(p2_rect.x,p2_rect.y - 10, int(p2_width*shield_pct),5))

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
       
        
        
        # Player 1 Attack (F key)
        if keys[pygame.K_f] and p1_attack_cooldown == 0 and not p1_is_blocking:
            punch_sound.play() # Play swing sound
            # Attack box extends 40px out from player_rect
            p1_attack_rect = pygame.Rect(player_rect.right, player_rect.y + 20, 40, 20)
            pygame.draw.rect(screen, (255, 255, 0), p1_attack_rect)  # Visual punch indicator (Yellow)

    
            # Check if attack box hits Player 2
            if p1_attack_rect.colliderect(p2_rect):
                if p2_is_blocking == True:
                    p2_health -= 0
                    block_sound.play() # Play block sound
                    spawn_particles(p2_rect.left, p2_rect.y + 30, (0, 200, 255), count=8)
                else:
                    hit_sound.play() # Play hit sound
                    p2_health -=  10
                    p1_attack_cooldown = 30
                    p2_rect.x += 20  # Knockback Player 2 to the right
                    spawn_particles(p2_rect.left, p2_rect.y + 30, (255, 255, 0), count=12)
        # Player 2 Attack (L key)
        if keys[pygame.K_l]and p2_attack_cooldown == 0 and not p2_is_blocking:
            # Attack box extends 40px out from player_rect
            punch_sound.play() # Play swing sound
            p2_attack_rect = pygame.Rect(p2_rect.left - 40, p2_rect.y + 20, 40, 20)
            pygame.draw.rect(screen, (255, 255, 0), p2_attack_rect)  # Visual punch indicator (Yellow)

            # Check if attack box hits Player 1
            if p2_attack_rect.colliderect(player_rect):
                if p1_is_blocking == True:
                    block_sound.play() # Play block sound
                    p1_health -= 0
                    spawn_particles(player_rect.right, player_rect.y + 30, (0, 200, 255), count=8)
                else:
                    hit_sound.play() # Play hit sound
                    p1_health -= 10
                    p2_attack_cooldown = 30
                    player_rect.x -= 20  # Knockback Player 1 to the left
                    spawn_particles(player_rect.right, player_rect.y + 30, (255, 255, 0), count=12)
        if p1_attack_cooldown > 0:
            p1_attack_cooldown  -= 1

        if p2_attack_cooldown > 0:
            p2_attack_cooldown -= 1
        if keys[pygame.K_g] and p1_fireball_cd == 0 and p1_fireball == None and  not p1_is_blocking:
            p1_fireball = pygame.Rect(player_rect.right, player_rect.y + 30, 20, 20)
            p1_fireball_cd = 120   # 2-second cooldown (120 frames at 60 FPS)
            fireball_sound.play() # Play fireball sound
        if keys[pygame.K_k] and p2_fireball_cd == 0 and p2_fireball == None and not p2_is_blocking:
            p2_fireball = pygame.Rect(p2_rect.left - 20, p2_rect.y + 30, 20, 20)
            p2_fireball_cd = 120   # 2-second cooldown (120 frames at 60 FPS)
            fireball_sound.play() # Play fireball sound
        # --- Player 1 Fireball Logic --- [G key]
        if p1_fireball != None:
            p1_fireball.x += p1_fireball_speed
            # Check hit on Player 2
            if p1_fireball.colliderect(p2_rect):
                if p2_is_blocking:
                    block_sound.play() # Play block sound
                    spawn_particles(p1_fireball.x, p1_fireball.y, (50,255,50), count=8)
                    p1_fireball = None
                    
                else:
                    hit_sound.play() # Play hit sound
                    p2_health -= 15            # Fireballs deal 15 damage!
                    p2_rect.x += 30            # Extra knockback
                    spawn_particles(p1_fireball.x, p1_fireball.y, (255, 100, 0), count=15)
                    p1_fireball = None         # Destroy fireball on impact
                    
            # Remove if off-screen
            else:
                if p1_fireball.left > SCREEN_WIDTH:
                    p1_fireball = None
        # --- Player 2 Fireball Logic --- [K key]
        if p2_fireball != None:
            p2_fireball.x += p2_fireball_speed
            # Check hit on Player 1
            if p2_fireball.colliderect(player_rect):
                if p1_is_blocking:
                    spawn_particles(p2_fireball.x, p2_fireball.y, (50,255,50), count=8)
                    p2_fireball = None
                    block_sound.play() # Play block sound
                    
                else:
                    p1_health -= 15            # Fireballs deal 15 damage!
                    player_rect.x -= 30            # Extra knockback
                    spawn_particles(p2_fireball.x, p2_fireball.y, (255,100,0), count=15)
                    p2_fireball = None         # Destroy fireball on impact
                    hit_sound.play() # Play hit sound
                    
            # Remove if off-screen
            else:
                if p2_fireball.right < 0:
                    p2_fireball = None
                
        p1_old_x = player_rect.x
        p2_old_x = p2_rect.x
        # Player 1 Movement
        if keys[pygame.K_a] and not p1_is_blocking:
            player_rect.x -= player_speed


        if keys[pygame.K_d] and not p1_is_blocking:
            player_rect.x += player_speed
            
        # Player 2  Movement
        if keys[pygame.K_LEFT] and not p2_is_blocking:
            p2_rect.x -= player_speed

        

        if keys[pygame.K_RIGHT] and not p2_is_blocking:
            p2_rect.x += player_speed

        if player_rect.colliderect(p2_rect):
            if p1_old_x < p2_old_x:
                bump_sound.play() #play bump sound
                player_rect.x = p1_old_x - 15
                p2_rect.x = p2_old_x + 15
            else:
                bump_sound.play()   #play bump sound
                player_rect.x = p1_old_x + 15
                p2_rect.x = p2_old_x - 15
        # Player 1 Jump
        if keys[pygame.K_w] and not is_jumping and not p1_is_blocking:
            vel_y = JUMP_STRENGTH
            is_jumping = True

        # Player 2 Jump
        if keys[pygame.K_UP] and not p2_is_jumping and not p2_is_blocking:
            p2_vel_y = JUMP_STRENGTH
            p2_is_jumping = True
        if round_time <= 0 and not game_over:
            game_over = True
            pygame.mixer.music.fadeout(1000)  # Fade out music on Time Over
            if p1_health > p2_health:
                p1_score += 1
                winner_text = "Time Over! Kashan Wins!"
            elif p2_health > p1_health:
                 p2_score += 1
                 winner_text = "Time Over! Ali Wins!"
            else:
                winner_text = "Time Over! Draw!"

    

    # Reduce cooldown timer every frame
    if p1_fireball_cd > 0:
        p1_fireball_cd -= 1
    if p2_fireball_cd > 0:
        p2_fireball_cd -= 1
    if p1_fireball != None:
        pygame.draw.rect(screen, (255, 165, 0), p1_fireball)
    if p2_fireball != None:
        pygame.draw.rect(screen, (255, 165, 0), p2_fireball)
    

    # Draw Rectangles
    pygame.draw.rect(screen, (255, 0, 0), player_rect)
    pygame.draw.rect(screen, (255, 0, 0), player_rect,3)
    pygame.draw.rect(screen, (0, 0, 255), p2_rect)
    pygame.draw.rect(screen, (0, 0, 255), p2_rect,3)
    pygame.draw.line(screen,(200,200,220),(0,500),(1000,500),10)
    pygame.draw.rect(screen, (255, 255, 255), p1_eye_rect)
    pygame.draw.rect(screen, (255, 255, 255), p2_eye_rect)
    pygame.draw.rect(screen, (255, 255, 255), p1_nose_rect)
    pygame.draw.rect(screen, (255, 255, 255), p2_nose_rect)
    pygame.draw.rect(screen, (0,255,0), grass_rect)
    pygame.draw.rect(screen, (255, 255, 255), p1_hand_rect)
    pygame.draw.rect(screen, (255, 255, 255), p2_hand_rect)
    # Draw Player 1 Shield
    if p1_is_blocking == True:
        # Slightly larger rectangle surrounding player_rect
        p1_shield_rect = pygame.Rect(player_rect.x - 5, player_rect.y - 5, player_width + 10, player_height + 10)
        pygame.draw.rect(screen, (255, 255, 255), p1_shield_rect,4)
        

    if p2_is_blocking:
        p2_shield_rect = pygame.Rect(p2_rect.x - 5, p2_rect.y - 5, p2_width + 10, p2_height + 10)
        pygame.draw.rect(screen, (255, 255, 255), p2_shield_rect,4)
        

    # Draw text labels on top
    p1_text = font.render("Kashan Intekhab", True, (255, 255, 255))
    p2_text = font.render("Ali Hammad", True, (255, 255, 255))
    score_text = font.render(f"Kashan: {p1_score}  |  Ali: {p2_score}", True, (255, 255, 255))
    hp_tag = font.render("HP", True, (255, 255, 255))
    timer_surface = large_font.render(str(round_time), True, (255, 255, 255))
    screen.blit(timer_surface, (SCREEN_WIDTH // 2 - 20, 50))

    screen.blit(p1_text, (player_rect.x - 20, player_rect.y - 25))
    screen.blit(p2_text, (p2_rect.x - 10, p2_rect.y - 25))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - 80, 20))
    screen.blit(hp_tag, (3, 22))                      # P1 HP Tag
    screen.blit(hp_tag, (SCREEN_WIDTH - 358, 22))      # P2 HP Tag

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

    if game_over == True:
            large_winner_surface = large_font.render(winner_text,True,(255,255,255))
            restart_prompt = small_font.render("Press R to Restart",True,(255,255,255))
            # Center text on screen
            screen.blit(large_winner_surface, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
            screen.blit(restart_prompt, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20))
    

    
    if game_over and keys[pygame.K_r]:
        p1_health = MAX_HEALTH
        p2_health = MAX_HEALTH
        player_rect = pygame.Rect(player_x,player_y,player_width,player_height)
        p2_rect = pygame.Rect(p2_x, p2_y, p2_width, p2_height)
        vel_y = 0
        p2_vel_y = 0
        p1_attack_cooldown = 0
        p2_attack_cooldown = 0
        game_over = False
        p1_fireball = None
        p2_fireball = None
        p1_fireball_cd = 0
        p2_fireball_cd = 0
        round_time = 60
        pygame.mixer.music.play(-1)  # Restart looping music for the new round
        match_intro_timer = 120
        round_number += 1

    
    for j in particles.copy():
        j["x"] += j["vel_x"]
        j['y'] += j["vel_y"]
        j['life'] -= 1 
        spawn_rect = pygame.Rect(j["x"], j["y"], j["size"],j["size"])
        pygame.draw.rect(screen, j["color"], spawn_rect)
        if j["life"] <= 0:
            particles.remove(j)

    # 4. Refresh Screen
    pygame.display.flip()

    # 3. Cap Frame Rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()