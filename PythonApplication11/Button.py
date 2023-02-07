from Common import *

#button class
class Button():
	def __init__(self, x, y, image):
		"""
		This function define the button
		Input : x,y - position; image - button's image display on the screen
		Output: Button's image on the screen and can interact by using mouse
		"""
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self,screen):
		"""
		This function draw the button to screen
		and get action if the button get clicked by left mouse
		"""
		action = False
		
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #[0] means left mouse click
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		screen.blit(self.image, self.rect)

		return action

