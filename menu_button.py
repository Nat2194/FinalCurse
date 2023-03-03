import pygame

# button class

class Button():
	def __init__(self, x, y, image, scale, place):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		if place == "topleft":
			self.rect.topleft = (x, y)
		elif place == "top":
			self.rect.top = (x, y)
		elif place == "topright":
			self.rect.topright = (x, y)
		elif place == "center":
			self.rect.center = (x,y)
		elif place == "bottomleft":
			self.rect.bottomleft = (x, y)
		elif place == "bottom":
			self.rect.bottom = (x, y)
		elif place == "bottomright":
			self.rect.bottomright = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False

		# get mouse position
		pos = pygame.mouse.get_pos()

		# check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
				action = True
				self.clicked = True

		if not pygame.mouse.get_pressed()[0]:
			self.clicked = False

		# draw button
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action
