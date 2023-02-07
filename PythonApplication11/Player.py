from Common import *

#player class
class Player():
	def __init__(self, x, y, image):
		"""
		This function define player
		Input : x,y - position; image - player's image display on the screen
		Output: Player's variables
		"""
		self.image = pygame.transform.scale(image, (45, 45))
		self.width = 25  #player's rectangle width                 
		self.height = 40 #player's rectangle height                 
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = (x, y)
		self.vel_y = 0   #player's velocity
		self.flip_x = False #check if player can flip left/right
		self.isJump = False
		

	def move(self):
		"""
		This function define player's movement
		The player can move and jump using keyboard, fall by gravity
		When the player jump up reach the scroll_threshold, it makes the background and others entities scroll down
		"""
		#reset variables
		scroll = 0
		self.dx = 0
		self.dy = 0

		#process keypresses
		key = pygame.key.get_pressed()
		if key[pygame.K_a]:
			self.dx = -7
			self.flip_x = True
		if key[pygame.K_d]:
			self.dx = 7
			self.flip_x = False
		if not(self.isJump):
			if key[pygame.K_w]:
				self.isJump = True 
				self.vel_y = -17
			
		#gravity - make player falling
		self.vel_y += GRAVITY
		self.dy += self.vel_y
		self.isJump = True #disable jumping when falling

		#ensure player doesn't go off the edge of the screen
		if self.rect.left + self.dx < 60:
			self.dx = -self.rect.left + 60
		if self.rect.right + self.dx > SCREEN_WIDTH - 60:
			self.dx = SCREEN_WIDTH - 60 - self.rect.right
			
		#check if the player has bounced to the Threshold then scroll
		if self.rect.top <= SCROLL_THRESHOLD:
			#if player is jumping
			if self.vel_y < 0:
				scroll = -self.dy
				self.isJump = True 

		#update rectangle position
		self.rect.x += self.dx
		self.rect.y += self.dy + scroll

		#create mask for perfect fast collision detection
		self.mask = pygame.mask.from_surface(self.image)

		return scroll

	def draw(self,screen):
		screen.blit(pygame.transform.flip(self.image, self.flip_x, False), (self.rect.x - 10, self.rect.y - 5)) #render the player and make it fit it's rectangle
		#draw player's rectangle
		#pygame.draw.rect(screen, WHITE, self.rect, 2)


