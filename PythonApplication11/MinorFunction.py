from Common import *

pygame.font.init()

#define font
font = pygame.font.SysFont('Times New Roman',24)

#Function to render text to screen
def draw_text(text,font,text_color,x,y,screen):
	img = font.render(text,True,text_color)
	screen.blit(img,(x,y))

#Function to draw panel show score in screen	
def draw_support(screen,score):
	pygame.draw.rect(screen, CYAN, (0, 0, SCREEN_WIDTH, 30))
	draw_text('SCORE: ' + str(score), font, WHITE, 0, 0,screen)

#Function to draw background(loop)
def draw_bg(bg_scroll,screen,image):
	screen.blit(image, (0, 0 + bg_scroll))
	screen.blit(image, (0, -600 + bg_scroll))