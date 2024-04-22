import random
import sys

import pygame

# Contants
WIDTH, HEIGHT = (800, 600)
JUMP_HEIGHT = 20
OBS_SPEED = 5
OBS_DEFAULT_SPEED = 5
OBS_ACCELERATOR = 0.0003
OBS_MAX_SPEED = 25
SPAWN_TIME = 2000
# End of contants

# Variables
gravity = 0
is_active = False
start_time = 0
score = 0

# Functions
def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score = current_time // 100
    score_surf = text_font.render(f'{score}', False, 'black')
    score_rect = score_surf.get_rect(midtop=(WIDTH//2, 40))
    screen.blit(score_surf, score_rect)
    return score


def move_obstacles(snail_list):
    if snail_list:
        for rect in snail_list:
            rect.x -= OBS_SPEED

            if rect.midbottom[1] == 400:
                screen.blit(snail_surf, rect)
            else:
                screen.blit(fly_surf, rect)
        
        new_list = [rect for rect in snail_list if rect.x > -100]

        return new_list
    return []

def collide_obstacles(player, obstacles):
    if len(obstacles) == 0: 
        return False
    for obstacle_rect in obstacles:
        if player.colliderect(obstacle_rect):
            return True
    return False


pygame.init()

# Display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Run!')
# End of display

# Surface
## Ground surface
ground_surf = pygame.Surface((WIDTH, 200))
ground_surf.fill('lightgreen')
ground_rect = ground_surf.get_rect(bottomleft=(0, HEIGHT))

## Sky surface
sky_surf = pygame.Surface((WIDTH, HEIGHT))
sky_surf.fill('lightblue')
sky_rect = sky_surf.get_rect(topleft=(0, 0))

## Cloud surface
cloud_surf = pygame.Surface((120, 60))
cloud_surf.fill('mintcream')
cloud_rect = cloud_surf.get_rect(topleft=(500, 20))

## Player surface
player_surf = pygame.Surface((60, 100))
player_surf.fill('indianred')
player_rect = player_surf.get_rect(midbottom=(100, 400))

## Intro screen's surface
player_stand_rect = player_surf.get_rect(center=(WIDTH//2, HEIGHT//1.8))
intro_font = pygame.font.Font(None, 30)
title_font = pygame.font.Font(None, 50)
game_title_surf = title_font.render('that runner game!', True, (64, 64, 64))
game_title_rect = game_title_surf.get_rect(midtop=(WIDTH//2, 120))
greeting_text_surf = intro_font.render('press space to start', True, (64, 64, 64))
greeting_text_rect = greeting_text_surf.get_rect(midtop=(WIDTH//2, 400))

## Snail surface
snail_surf = pygame.Surface((80, 40))
snail_surf.fill('plum')
## Fly surface
fly_surf = pygame.Surface((60, 20))
fly_surf.fill('lightslategrey')
# End of Surface

# Fonts
text_font = pygame.font.Font(None, 50)
# End of Fonts

# Pygame clock
clock = pygame.time.Clock()

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, SPAWN_TIME)

# Obstacle list
obstacle_rect_list = []

while True:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Game is running
        if is_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= ground_rect.top:
                    gravity = -JUMP_HEIGHT
            if event.type == obstacle_timer:
                rand_x = random.randint(WIDTH + 100, WIDTH + 300)
                if random.randint(0, 1):
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom=(rand_x, 400)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(midbottom=(rand_x, 260)))
        # Game has stopped
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    obstacle_rect_list = []
                    is_active = True
                    start_time = pygame.time.get_ticks()
                    OBS_SPEED = OBS_DEFAULT_SPEED
    # End of Events
    
    if is_active:
        # Draw surface on screen (use blit to draw image onto another)
        screen.blit(sky_surf, sky_rect)
        screen.blit(cloud_surf, cloud_rect)
        screen.blit(ground_surf, ground_rect)
        screen.blit(player_surf, player_rect)
        score = display_score()
        # End of Drawing on screen

        # Movement
        ## Snail movement
        OBS_SPEED = min(OBS_SPEED + OBS_ACCELERATOR, OBS_MAX_SPEED)
        obstacle_rect_list = move_obstacles(obstacle_rect_list)
        ## Player movement
        gravity += 1
        player_rect.y += gravity
        if player_rect.bottom >= ground_rect.top:
            player_rect.bottom = ground_rect.top
        ## Cloud movement
        cloud_rect.x -= 1
        if cloud_rect.right < 0:
            cloud_rect.left = WIDTH
        # End of Movement

        # Collision
        is_active = not collide_obstacles(player_rect, obstacle_rect_list)
    else:
        screen.fill('lightgreen')
        screen.blit(player_surf, player_stand_rect)
        screen.blit(game_title_surf, game_title_rect)
        screen.blit(greeting_text_surf, greeting_text_rect)
        
        last_score_surf = intro_font.render(f'score: {score}', True, (64, 64, 64))
        last_score_rect = last_score_surf.get_rect(midtop=game_title_rect.midbottom)
        screen.blit(last_score_surf, last_score_rect)

    pygame.display.update()
    clock.tick(60)