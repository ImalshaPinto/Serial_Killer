import pygame
from main_character import MainCharacter  # Import the MainCharacter class

# Initialize pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((1250, 700))

# Title and Icon
pygame.display.set_caption("Skull Killer")
icon = pygame.image.load('backgroundLevel1.jpg')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('palacegrounds.png')
background = pygame.transform.scale(background, (1250, 700))

# Load the sprite sheet
sprite_sheet = pygame.image.load('Scorpian/last.png')
sprite_sheet2 = pygame.image.load('Scorpian/Srunning.png')
sprite_sheet3 = pygame.image.load('Scorpian/duck&up.png')
sprite_sheet4 = pygame.image.load('Scorpian/jumpfront3.png')
sprite_sheet5 = pygame.image.load('Scorpian/jump.png')

# Game loop
running = True
clock = pygame.time.Clock()
player = MainCharacter(370, 350)

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x_change = -3
            if event.key == pygame.K_RIGHT:
                player.x_change = 3
            if event.key == pygame.K_DOWN:
                player.is_ducking = True
                player.is_getting_up = False
                player.frame_index = 0
            if event.key == pygame.K_UP:
                if player.x_change != 0:  # Directional jump
                    player.is_jumping_directional = True
                else:  # Vertical jump
                    player.is_jumping_vertical = True
                player.frame_index = 0
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player.x_change = 0
            if event.key == pygame.K_DOWN:
                player.is_ducking = False
                player.is_getting_up = True
                player.frame_index = 0

    player.update_position()
    player.update_frame()
    player.draw()

    pygame.display.update()
    clock.tick(60)

pygame.quit()