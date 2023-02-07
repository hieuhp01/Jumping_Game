from Common import *

#platform class
class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, width, move_x, move_y, speed, image):
		"""
		This function define the platform
		Input : x,y - position; image - button's image display on the screen
		        width of the platform; move_x, move_y - the ability to move horizontaly and vertically
				speed of the platform if it's moving; platform's image display on the screen
		Output: Platform which can move/stay, display on the screen 
		"""
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(image, (width, 10))
		self.move_x = move_x
		self.move_y = move_y
		self.move_counter = random.randint(0,50)
		self.direction = random.choice([-1,1])
		self.speed = speed
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, scroll):
		"""
		This function define the moving ability of platform
		Input : scroll to update platform's vertical position 
		Output: Decide the movement of platform and delete it when out of the screen
		"""
		#moving platform horizontal if it is a moving platform
		if self.move_x == True:
			self.move_counter += 1
			self.rect.x += self.direction * self.speed

        #moving platform vertical if it is a moving platform
		if self.move_y == True:
			self.move_counter += 1
			self.rect.y += self.direction * self.speed

		#change platform direction if it has moved fully or hit a wall
		if self.move_counter >= random.randint(60,100) or self.rect.left < 60 or self.rect.right > SCREEN_WIDTH - 60:
			self.direction *= -1
			self.move_counter = 0

		#update platform's vertical position
		self.rect.y += scroll

		#check if platform has gone off the screen then delete it 
		if self.rect.top > SCREEN_HEIGHT:
			self.kill()






