import os
from LoadMedia import *

#initialise pygame
pygame.init()

#set frame rate
clock = pygame.time.Clock()
FPS = 60

#create file for saving highscore
if os.path.exists('score.txt'):
	with open('score.txt', 'r') as file:
		high_score = int(file.read())
else:
	high_score = 0

#Function to draw background(loop)
def draw_bg(bg_scroll,screen):
	screen.blit(bg_image1, (0, 0 + bg_scroll))
	screen.blit(bg_image2, (0, -600 + bg_scroll))
	screen.blit(bg_image2, (0, -1200 + bg_scroll))
#game loop
if __name__ == "__main__":
	run = True
	while run:

		clock.tick(FPS)
		
		if main_menu == True:
			"""
			This function display the main menu with 4 options:
			start, option, more and exit
			"""
			screen.blit(bg_image1, (0,0)) #display background for main menu
			if menu_state == "main":
				if exit_button.draw(screen): #click exit button to close application
					run = False
				if start_button.draw(screen): #click start button to play
					main_menu = False 
				if option_button.draw(screen): #click option button to show how to play
					menu_state = "guide"
				if more_button.draw(screen): #click more button to show highestscore
					menu_state = "highscore"
			if menu_state == "guide": #show how to play game
				draw_text("Press A and D to move", font, RED, 100,SCREEN_HEIGHT//2 - 100,screen)
				draw_text("Press W to jump", font, RED, 125,SCREEN_HEIGHT//2,screen)
				if back_button.draw(screen): #click back button to return to main menu
					menu_state = "main"
			if menu_state == "highscore": #show highscore
				draw_text("HIGHEST SCORE: " + str(high_score), font, RED, 75, 300,screen)
				if back_button.draw(screen):
					menu_state = "main" #click back button to return to main menu
		else:
			"""
			This function is the mainloop of the game:
			- Generate infinite scrolling background based on player_jump and panel show score on top of the screen
			- Display platforms, enemies, player 
			- Detect collision between player and platforms, enemies
			- Game over when player fall off the screen and when player collide with enemies
			- Display options when Game over
			"""
			if game_over == False:
				scroll = player.move()

				#draw background(infinite scroll based on player_jump)
				bg_scroll += scroll
				if bg_scroll >= 1200:
					bg_scroll = 600
				draw_bg(bg_scroll,screen)

				#draw scroll threshold
				#pygame.draw.line(screen, WHITE, (0, SCROLL_THRESHOLD), (SCREEN_WIDTH, SCROLL_THRESHOLD))

				#generate platforms
				if len(platform_group) < MAX_PLATFORMS:
					p_w = random.randint(40, 60)
					p_x = random.randint(60, SCREEN_WIDTH - 60 - p_w)
					p_y = platform.rect.y - random.randint(60, 120) #each platform distance from each other vertically 
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
					platform = Platform(p_x, p_y, p_w, p_move_x, p_move_y, p_speed, platform_image)
					platform_group.add(platform)

				#update platforms
				platform_group.update(scroll)
				#check collision between player and platforms
				player.collisionP(platform,platform_group)

				#generate enemies
				if len(enemy_group) == 0 and score > 3000 and score < 8000:
					enemy = Enemy(random.randint(0, 450),enemy_image) #generate 1 enemy each screen
					#check if enemy always appears above player
					if player.rect.top > enemy.rect.bottom:
						enemy_group.add(enemy)
				elif len(enemy_group) < MAX_ENEMY and score > 8000:
					enemy = Enemy(random.randint(0, 450), enemy_image) #generate 1-2 enemies each screen
					#check if enemy always appears above player
					if player.rect.top > enemy.rect.bottom:
						enemy_group.add(enemy)
			   
				#update enemies
				enemy_group.update(scroll)

				#update score
				if scroll > 0:
					score += scroll

				#draw line at previous high score
				#pygame.draw.line(screen, WHITE, (0, score - high_score + SCROLL_THRESHOLD), (SCREEN_WIDTH, score - high_score + SCROLL_THRESHOLD), 3)
				#draw_text("HIGH SCORE", font, WHITE, SCREEN_WIDTH - 170, score - high_score + SCROLL_THRESHOLD,screen)

				#draw sprites
				platform_group.draw(screen)
				enemy_group.draw(screen)
				player.draw(screen)
				
				#draw enemy rectangle
				#for enemy in enemy_group:
					#pygame.draw.rect(screen, WHITE, enemy.rect, 2)
		
				#draw support
				draw_support(screen,score)

				#check game over
				if player.rect.top > SCREEN_HEIGHT:
					game_over = True
				#check game over if collide with enemy
				if pygame.sprite.spritecollide(player,enemy_group,False, pygame.sprite.collide_mask):
					game_over = True
			else:
				
				#when game over show
				pygame.time.delay(150)
				pygame.draw.rect(screen,BLACK,([0,0,400,600]))
				draw_text("GAME OVER!",font,WHITE,130,200,screen)
				draw_text("SCORE: " + str(score),font,WHITE,130,250,screen)
				draw_text("HIGHEST SCORE: " + str(high_score),font,WHITE,75,300,screen)
				draw_text("PRESS R TO PLAY AGAIN",font,WHITE,65,350,screen)
				draw_text("PRESS ESC TO MAIN MENU",font,WHITE,60,400,screen)

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
					bg_scroll =0 
					player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
					platform_group.empty()
					enemy_group.empty()
					platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False, False, False, platform_image)
					platform_group.add(platform)
				#Press space to back to main menu
				if key[pygame.K_ESCAPE]:
					#reset variables and back to main menu
					game_over = False
					score = 0
					scroll = 0
					bg_scroll =0
					player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
					platform_group.empty()
					enemy_group.empty()
					platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False, False, False, platform_image)
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
