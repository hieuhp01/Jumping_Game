from Common import *

#define font
pygame.font.init()
font = pygame.font.SysFont('Times New Roman',24)

#Function to render text to screen
def draw_text(text,font,text_color,x,y,screen):
	img = font.render(text,True,text_color)
	screen.blit(img,(x,y))

#Function to draw panel show score in screen	
def draw_support(screen,score):
	pygame.draw.rect(screen, CYAN, (0, 0, SCREEN_WIDTH, 30))
	draw_text('SCORE: ' + str(score), font, WHITE, 0, 0,screen)
	


	
	