from Common import *
from Enemy import Enemy
from Platform import Platform
from Button import Button
from Player import Player
from MinorFunction import *

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('GAME V1.0')

#load and scale images player, background, platforms, enemies, button
player_image = pygame.image.load('assets/Pink_Monster.png').convert_alpha()

bg_image1 = pygame.image.load('assets/04_BG_Preview_With_Start.png').convert_alpha()
bg_image1 = pygame.transform.scale(bg_image1,(400,600))
bg_image2 = pygame.image.load('assets/04_BG_Preview_Without_Start.png').convert_alpha()
bg_image2 = pygame.transform.scale(bg_image2,(400,600))

platform_image = pygame.image.load('assets/Pad_1_1.png').convert_alpha()
enemy_image = pygame.image.load('assets/spike_ball_by_lwiis64_df30ssj.png').convert_alpha()

start_image = pygame.image.load('assets/Start_Button.png').convert_alpha()
start_image = pygame.transform.scale(start_image,(100,50))
exit_image = pygame.image.load('assets/ExitButton.png').convert_alpha()
exit_image = pygame.transform.scale(exit_image,(100,50))
option_image = pygame.image.load('assets/Option_Button.png').convert_alpha()
option_image = pygame.transform.scale(option_image,(100,50))
more_image = pygame.image.load('assets/More_Button.png').convert_alpha()
more_image = pygame.transform.scale(more_image,(100,50))
back_image = pygame.image.load('assets/Back_Button.png').convert_alpha()
back_image = pygame.transform.scale(back_image,(50,50))

#create buttons
start_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100, start_image)
exit_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, exit_image)
option_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50, option_image)
more_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 , more_image)
back_button = Button(SCREEN_WIDTH -125, SCREEN_HEIGHT -100, back_image)
				   
#player init position
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, player_image)

#create sprite groups for handling platforms and enemies
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

#create starting platform
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False, False, False, platform_image)
platform_group.add(platform)

