# Action types: up, down, left, right, space, enter

_ACTION_BY_PYGAME_EVENT = {
	pygame.K_UP: 'up',
	pygame.K_DOWN: 'down',
	pygame.K_RIGHT: 'right',
	pygame.K_LEFT: 'left',
	pygame.K_RETURN: 'enter',
	pygame.K_SPACE: 'space',
	pygame.K_LALT: 'lalt',
	pygame.K_RALT: 'ralt',
}

class Action:
	def __init__(self, type, down):
		self.type = type
		self.down = down
		self.up = not down

class Engine:
	def __init__(self):
		self.screen = None
		self.width = None
		self.height = None
		self.title = 'Window'
		self.isFullScreen = False
		self.exitGame = False
		self.pressedActions = {}
		self.frameStart = None
		self.screenAlpha = 1.0
		self.blackener = None
		for type in 'up down left right space enter f4'.split(' '):
			self.pressedActions[type] = False
			
	
	def openWindow(self, title, width, height):
		pygame.init()
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption(title)
	
	def toggleFullScreen(self):
		if self.isFullScreen:
			self.screen = pygame.display.set_mode((width, height))
		else:
			self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
		self.isFullScreen = not self.isFullScreen
	
	def quit(self):
		self.exitGame = Truue
	
	def pumpEvents(self):
		
		events = []
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.exitGame = True
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_F4 and (self.pressedActions['lalt'] or self.pressedActions['ralt']):
					self.exitGame = True
				
				if event.key == pygame.K_p:
					self.toggleFullScreen()
					
			if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
				action = _ACTION_BY_PYGAME_EVENT.get(event.key)
				if action != None:
					down = event.type == pygame.KEYDOWN
					self.pressedActions[action] = down
					events.append(Action(action, down))
			
		return events
	
	def setScreenAlpha(self, value):
		if value < 0: value = 0
		if value > 1: value = 1
		self.screenAlpha = value
	
	def clockTick(self):
		alpha = int(self.screenAlpha * 255 + .5)
		if alpha < 255:
			overlay = self.blackener
			if overlay == None:
				overlay = self.screen.convert()
				self.blackener = overlay
			overlay.set_alpha(255 - alpha)
			self.screen.blit(overlay, (0, 0))
			
		pygame.display.flip()
		if self.frameStart == None:
			self.frameStart = time.time()
		else:
			now = time.time()
			diff = now - self.frameStart
			delay = 1 / 30.0 - diff
			if delay > 0:
				time.sleep(delay)
			self.frameStart = now
	
	def fill(self, r, g, b):
		self.screen.fill((r, g, b))
	
	def drawImageInstance(self, img, x, y):
		self.screen.blit(img, (x, y))
	
	def drawImageTopLeft(self, path, x, y):
		self.screen.blit(IMAGES.get(path), (x, y))
	
	def drawImage(self, path, x, y, angle = None):
		if angle == None:
			img = IMAGES.get(path)
		else:
			img = IMAGES.getRotated(path, angle)
		
		w, h = img.get_size()
		x -= w / 2.0
		y -= h / 2.0
		
		self.screen.blit(img, (int(x), int(y)))
	
	def drawImageWithRotationalOffset(self, path, x, y, radius, angle):
		pass
	
Q = Engine()