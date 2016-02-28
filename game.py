import pygame
import math
import time
import random
import os



class ImageLibrary:
	def __init__(self):
		self.images = {}
	
	def get(self, path):
		return None

IMAGES = ImageLibrary()





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
		
	



def main():
	
	pygame.init()
	
	screen = pygame.display.set_mode((800, 600))
	
	scene = TitleScene()
	rc = 0
	events = []
	pressed_keys = {}
	while True:
		start = time.time()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			
			if event.type == pygame.KEYDOWN:
				pressed_keys[event.key] = True
				if event.key == pygame.K_F4 and (pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]):
					return
			if event.type == pygame.KEYUP:
				pressed_keys[event.key] = False
		
		scene.update(events, pressed_keys)
		scene.render(screen, rc)
		rc += 1
		pygame.display.flip()
		end = time.time()
		diff = end - start
		delay = 1 / 30.0 - diff
		if delay > 0:
			time.sleep(delay)
			
main()
