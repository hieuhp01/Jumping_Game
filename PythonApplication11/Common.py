import pygame
import random

pygame.font.init()

#game window dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

#game variables
SCROLL_THRESHOLD = 200
GRAVITY = 1
MAX_PLATFORMS = 10
MAX_ENEMY = 2
scroll = 0
bg_scroll = 0
game_over = False
main_menu = True
menu_state = "main"
score = 0

#define colours
WHITE = (255, 255, 255)
CYAN = (0, 100, 100)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


#define font
font = pygame.font.SysFont('Times New Roman',24)


