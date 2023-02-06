import pygame
import random
import os

#initialise pygame
pygame.init()

#game window dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('GAME V1.0')

#set frame rate
clock = pygame.time.Clock()
FPS = 60

#game variables
SCROLL_THRESH = 200
GRAVITY = 1
MAX_PLATFORMS = 10
MAX_ENEMY = 2
scroll = 0
bg_scroll = 0
game_over = False
main_menu = True
menu_state = "main"
score = 0

#create file for saving highscore
if os.path.exists('score.txt'):
	with open('score.txt', 'r') as file:
		high_score = int(file.read())
else:
	high_score = 0

#define colours
WHITE = (255, 255, 255)
CYAN = (0, 100, 100)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#define font
font = pygame.font.SysFont('Times New Roman',24)

#load images player, background, platforms, enemies, button
player_image = pygame.image.load('assets/Pink_Monster.png').convert_alpha()

bg_image1 = pygame.image.load('assets/04_BG_Preview_With_Start.png').convert_alpha()
bg_image1 = pygame.transform.scale(bg_image1,(400,600))
bg_image2 = pygame.image.load('assets/04_BG_Preview_Without_Start.png').convert_alpha()
bg_image2 = pygame.transform.scale(bg_image2,(400,600))

platform_image = pygame.image.load('assets/Pad_1_1.png').convert_alpha()
enemy_image = pygame.image.load('assets/spike_ball_by_lwiis64_df30ssj.png').convert_alpha()

start_image = pygame.image.load('assets/Start_Button.png').convert_alpha()
start_image = pygame.transform.scale(start_image,(100,50))
exit_image = pygame.image.load('assets/Exit_Button.png').convert_alpha()
exit_image = pygame.transform.scale(exit_image,(100,50))
guide_image = pygame.image.load('assets/Guide_Button.png').convert_alpha()
guide_image = pygame.transform.scale(guide_image,(100,50))
highscore_image = pygame.image.load('assets/More_Button.png').convert_alpha()
highscore_image = pygame.transform.scale(highscore_image,(100,50))
back_image = pygame.image.load('assets/Back_Button.png').convert_alpha()
back_image = pygame.transform.scale(back_image,(50,50))

#Function to render text to screen
def draw_text(text,font,text_color,x,y):
	img = font.render(text,True,text_color)
	screen.blit(img,(x,y))

#Function to draw panel show score in screen	
def draw_support():
	pygame.draw.rect(screen, CYAN, (0, 0, SCREEN_WIDTH, 30))
	draw_text('SCORE: ' + str(score), font, WHITE, 0, 0)

#Function to draw background(loop)
def draw_bg(bg_scroll):
	screen.blit(bg_image2, (0, 0 + bg_scroll))
	screen.blit(bg_image2, (0, -600 + bg_scroll))

#button class
class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False


		#draw button
		screen.blit(self.image, self.rect)

		return action

#player class
class Player():
	def __init__(self, x, y):
		self.image = pygame.transform.scale(player_image, (45, 45))
		self.width = 25
		self.height = 40
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = (x, y)
		self.vel_y = 0
		self.flip_x = False
		self.isJump = False
		

	def move(self):
		#reset variables
		scroll = 0
		dx = 0
		dy = 0

		#process keypresses
		key = pygame.key.get_pressed()
		if key[pygame.K_a]:
			dx = -10
			self.flip_x = True
		if key[pygame.K_d]:
			dx = 10
			self.flip_x = False
		if not(self.isJump):
			if key[pygame.K_w]:
				self.isJump = True 
				self.vel_y = -17
			
		#gravity
		self.vel_y += GRAVITY
		dy += self.vel_y
		self.isJump = True #disable jumping when falling

		#ensure player doesn't go off the edge of the screen
		if self.rect.left + dx < 60:
			dx = -self.rect.left + 60
		if self.rect.right + dx > SCREEN_WIDTH - 60:
			dx = SCREEN_WIDTH - 60 - self.rect.right

		#check collision with platforms
		for platform in platform_group:
			#collision in the y direction
			if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				#check if above the platform
				if self.rect.bottom < platform.rect.centery:
					if self.vel_y > 0:
						self.rect.bottom = platform.rect.top
						dy = 0
						self.vel_y = 0
						self.isJump = False #enable jumping when player stand above the platform
                                #move sideway with platform
				if platform.move_x != 0:
					self.rect.x += platform.direction
					
		#check if the player has bounced to the top of the screen
		if self.rect.top <= SCROLL_THRESH:
			#if player is jumping
			if self.vel_y < 0:
				scroll = -dy
				self.isJump = True 

		#update rectangle position
		self.rect.x += dx
		self.rect.y += dy + scroll

		#create mask for fast collision detection
		self.mask = pygame.mask.from_surface(self.image)

		return scroll

	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.flip_x, False), (self.rect.x - 12, self.rect.y - 4))
		


#platform class
class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, width, move_x, move_y, speed):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(platform_image, (width, 10))
		self.move_x = move_x
		self.move_y = move_y
		self.move_counter = random.randint(0,50)
		self.direction = random.choice([-1,1])
		self.speed = speed
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, scroll):

		#moving platform horizontal if it is a moving platform
		if self.move_x == True:
			self.move_counter += 1
			self.rect.x += self.direction * self.speed

        #moving platform vertical if it is a moving platform
		if self.move_y == True:
			self.move_counter += 1
			self.rect.y += self.direction * self.speed

		#change platform direction if it has moved fully or hit a wall
		if self.move_counter >= random.randint(60,150) or self.rect.left < 60 or self.rect.right > SCREEN_WIDTH - 60:
			self.direction *= -1
			self.move_counter = 0

		#update platform's vertical position
		self.rect.y += scroll

		#check if platform has gone off the screen then delete it 
		if self.rect.top > SCREEN_HEIGHT:
			self.kill()

class Enemy(pygame.sprite.Sprite):
	def __init__(self, y):
		pygame.sprite.Sprite.__init__(self)
		#define variables
		self.image = pygame.transform.scale(enemy_image, (40, 40))
		self.speed = random.randint(2,3)
		self.direction = random.choice([-1, 1])
		self.rect = self.image.get_rect()
		if self.direction == 1: #enemy move from left to right
			self.rect.x = 0
		else: #enemy move from right to left
			self.rect.x = SCREEN_WIDTH - 40

		self.rect.y = y

	def update(self, scroll):
		
		#move enemy
		self.rect.x += self.direction * self.speed
		self.rect.y += scroll

		#change enemy direction if it hit screen edge
		if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
			self.direction *= -1
			
                #check if enemy has gone off the screen then delete it
		if self.rect.top > SCREEN_HEIGHT:
			self.kill()

#create buttons
start_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100, start_image)
exit_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50, exit_image)
guide_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 -50, guide_image)
more_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 , highscore_image)
back_button = Button(SCREEN_WIDTH -125, SCREEN_HEIGHT -100, back_image)
				   
#player init position
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

#create sprite groups
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

#create starting platform
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False, False, False)
platform_group.add(platform)

#game loop
run = True
while run:

	clock.tick(FPS)

	screen.blit(bg_image1, (0,0))
	if main_menu == True:
		if menu_state == "main":
			if exit_button.draw(): #click exit button to close application
				run = False
			if start_button.draw(): #click start button to play
				main_menu = False 
			if guide_button.draw(): #click option button to show how to play
				menu_state = "guide"
			if more_button.draw(): #click more button to show highestscore
				menu_state = "highscore"
		if menu_state == "guide":
			draw_text("Press A and D to move", font, RED, 100,SCREEN_HEIGHT//2 - 100)
			draw_text("Press W to jump", font, RED, 125,SCREEN_HEIGHT//2)
			if back_button.draw():
				menu_state = "main"
		if menu_state == "highscore":
			draw_text("HIGHEST SCORE: " + str(high_score), font, RED, 75, 300)
			if back_button.draw():
				menu_state = "main"
	else:

		if game_over == False:
			scroll = player.move()

			#draw background(infinite scroll based on player_jump)
			bg_scroll += scroll
			if bg_scroll >= 600:
				bg_scroll = 0
			draw_bg(bg_scroll)

			#generate platforms
			if len(platform_group) < MAX_PLATFORMS:
				p_w = random.randint(40, 60)
				p_x = random.randint(60, SCREEN_WIDTH - 60 - p_w)
				p_y = platform.rect.y - random.randint(80, 120) #each platform distance from each other vertically 
				p_speed = 0
				p_type = random.randint(1, 4)
				if p_type == 1 and score > 3000: #platform moving side to side
					p_move_x = True
					p_move_y = False
					p_speed = 1
				elif p_type == 2 and score > 5000: #platform moving upside down
					p_move_x = False
					p_move_y = True
					p_speed = 2
				elif p_type == 3 and score > 10000: #platform moving along diagonal
					p_move_x = True
					p_move_y = True
					p_speed = 3
				else:
					p_move_x = False
					p_move_y = False
				platform = Platform(p_x, p_y, p_w, p_move_x, p_move_y, p_speed)
				platform_group.add(platform)

			#update platforms
			platform_group.update(scroll)

			#generate enemies
			if len(enemy_group) == 0 and score > 3000 and score < 8000:
				enemy = Enemy(random.randint(0, 450))
				#check if enemy always appears above player
				if player.rect.top > enemy.rect.bottom:
					enemy_group.add(enemy)
			elif len(enemy_group) < MAX_ENEMY and score > 8000:
				enemy = Enemy(random.randint(0, 450))
				#check if enemy always appears above player
				if player.rect.top > enemy.rect.bottom:
					enemy_group.add(enemy)
			   
			#update enemies
			enemy_group.update(scroll)

			#update score
			if scroll > 0:
				score += scroll

			#draw line at previous high score
			pygame.draw.line(screen, WHITE, (0, score - high_score + SCROLL_THRESH), (SCREEN_WIDTH, score - high_score + SCROLL_THRESH), 3)
			draw_text("HIGH SCORE", font, WHITE, SCREEN_WIDTH - 170, score - high_score + SCROLL_THRESH)

			#draw sprites
			platform_group.draw(screen)
			enemy_group.draw(screen)
			player.draw()
		

			#draw support
			draw_support()

			#check game over
			if player.rect.top > SCREEN_HEIGHT:
				game_over = True
			#check game over if collide with enemy
			if pygame.sprite.spritecollide(player, enemy_group, False):
				if pygame.sprite.spritecollide(player,enemy_group,False, pygame.sprite.collide_mask):
					game_over = True
		else:
			#when game over show
			pygame.draw.rect(screen,BLACK,([0,0,400,600]))
			draw_text("GAME OVER!",font,WHITE,130,200)
			draw_text("SCORE: " + str(score),font,WHITE,130,250)
			draw_text("HIGHEST SCORE: " + str(high_score),font,WHITE,75,300)
			draw_text("PRESS R TO PLAY AGAIN",font,WHITE,65,350)
			draw_text("PRESS ESC TO MAIN MENU",font,WHITE,60,400)

			#update high score
			if score > high_score:
				high_score = score
				with open('score.txt', 'w') as file:
					file.write(str(high_score))

			key=pygame.key.get_pressed()
			#Press r to replay
			if key[pygame.K_r]: 
				#reset variables
				game_over = False
				score = 0
				scroll = 0
				player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
				platform_group.empty()
				enemy_group.empty()
				platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False, False, False)
				platform_group.add(platform)
                        #Press space to back to main menu
			if key[pygame.K_ESCAPE]:
				#reset variables and back to main menu
				game_over = False
				score = 0
				scroll = 0
				player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
				platform_group.empty()
				enemy_group.empty()
				platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False, False, False)
				platform_group.add(platform)
				main_menu = True


	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			#update high score
			if score > high_score:
				high_score = score
				with open('score.txt', 'w') as file:
					file.write(str(high_score))
			run = False


	#update display window
	pygame.display.update()



pygame.quit()
