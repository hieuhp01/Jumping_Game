from Common import *

class Enemy(pygame.sprite.Sprite):
	def __init__(self, y, image):
		"""
		This function define the enemy
		Input : y - position to spawn the enemies; image(enemy)
		Output: display the enemy on the left/right of the screen along screen_height
		"""
		pygame.sprite.Sprite.__init__(self)
		#define variables
		self.image = pygame.transform.scale(image, (40, 40))
		self.speed = random.randint(2,3)
		self.direction = random.choice([-1, 1])
		self.rect = self.image.get_rect()
		if self.direction == 1: #enemy move from left to right
			self.rect.x = 0
		else: #enemy move from right to left
			self.rect.x = SCREEN_WIDTH - 40

		self.rect.y = y

	def update(self, scroll):
		"""
		This function define the movement of enemies
		Input : scroll to update enemy's vertical position 
		Output: enemy can move horizontally on the screen and disapear when out of the screen  
		"""
		#move enemy
		self.rect.x += self.direction * self.speed
		self.rect.y += scroll

		#change enemy direction if it hit screen edge
		if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
			self.direction *= -1
			
        #check if enemy has gone off the screen then delete it
		if self.rect.top > SCREEN_HEIGHT:
			self.kill()




