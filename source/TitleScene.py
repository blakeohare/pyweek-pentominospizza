import pygame

class TitleScene:
	def __init__(self):
		self.next = self
		self.quit_attempt = False
		self.x = 0
		self.y = 0
	
	def update(self, events, keys):
		self.x += 1
		self.y += 1
	
	def render(self, screen, rc):
		screen.fill((0, 0, 255))
		pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.x, self.y, 20, 20))
		
	