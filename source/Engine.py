# Action types: up, down, left, right, space, enter


class Action:
	def __init__(self, type, down):
		self.type = type
		self.down = down
		self.up = not down

class Engine:
	def __init__(self, pygame, pyglet):
		self.pygame = pygame
		self.pyglet = pyglet
		self.isPyglet = pyglet != None
		outerSelf = self
		self.fontEngine = None
		if self.isPyglet:
			class PygletWindow(pyglet.window.Window):
				def __init__(self, width, height, title):
					pyglet.window.Window.__init__(self, width, height, title)
				
				def on_draw(self):
					outerSelf.pygletOnDraw(self)
				
				def on_key_press(self, symbol, modifiers):
					outerSelf.pygletKeyEvent(symbol, True)
				
				def on_key_release(self, symbol, modifiers):
					outerSelf.pygletKeyEvent(symbol, False)
					
					
			self.windowClass = PygletWindow
			self._ACTION_BY_PYGLET_EVENT = {
				pyglet.window.key.UP: 'up',
				pyglet.window.key.DOWN: 'down',
				pyglet.window.key.LEFT: 'left',
				pyglet.window.key.RIGHT: 'right',
				pyglet.window.key.ENTER: 'enter',
				pyglet.window.key.SPACE: 'space',
			}
			self._FONT_SIZE_BY_SHIRT = {
				'XL': 36,
				'L': 20,
				'M': 14,
				'S': 10,
			}
		elif self.pygame != None:
			self._ACTION_BY_PYGAME_EVENT = {
					pygame.K_UP: 'up',
					pygame.K_DOWN: 'down',
					pygame.K_RIGHT: 'right',
					pygame.K_LEFT: 'left',
					pygame.K_RETURN: 'enter',
					pygame.K_SPACE: 'space',
					pygame.K_LALT: 'lalt',
					pygame.K_RALT: 'ralt',
				}
			print("Pyglet was not found. Falling back to PyGame. For better performance, please get Pyglet: https://bitbucket.org/pyglet/pyglet/wiki/Home")
		else:
			print("Neither PyGame nor Pyglet were found. One of these (preferably Pyglet) must exist in order to run.")
		
		self.initialized = False
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
		self.pygletEvents = []
		self.pygletThings = []
		for type in 'up down left right space enter f4'.split(' '):
			self.pressedActions[type] = False
	
	def pygletKeyEvent(self, symbol, isDown):
		key = self._ACTION_BY_PYGLET_EVENT.get(symbol)
		if key != None:
			self.pygletEvents.append(Action(key, isDown))
			self.pressedActions[key] = isDown
		
	def renderText(self, text, size, x, y):
		if self.isPyglet:
			size = self._FONT_SIZE_BY_SHIRT[size]
			label = self.pyglet.text.Label(text, font_name = 'Arial', font_size = size, x = x, y = self.height - y, anchor_x = 'left', anchor_y = 'top')
			self.pygletThings.append(label)
		else:
			if self.fontEngine == None:
				self.fontEngine = PyGameFontEngine()
			self.fontEngine.render(text, size, x, y)
	
	def pygletOnDraw(self, window):
		self.scene.render()
		window.clear()
		for thing in self.pygletThings:
			thing.draw()
		self.pygletThings = []
		
	def flushPygletEvents(self):
		if len(self.pygletEvents) > 0:
			output = self.pygletEvents
			self.pygletEvents = []
			return output
		return self.pygletEvents
	
	def pygletUpdate(self, dt):
		
		self.scene.update(self.flushPygletEvents(), dt)
		
		if self.scene != self.scene.next:
			old = self.scene
			self.scene = self.scene.next
			old.next = None
		
		
	def openWindow(self, title, width, height, scene):
		self.width = width
		self.height = height
		
		if self.isPyglet:
			self.window = self.windowClass(width, height, title)
			self.scene = scene
			self.pyglet.clock.schedule_interval(self.pygletUpdate, 1 / 60.0)
			self.pyglet.app.run()
		else:
			self.pygame.init()
			self.screen = self.pygame.display.set_mode((width, height))
			self.pygame.display.set_caption(title)
		
			while True:
				events = Q.pumpEvents()
				if Q.exitGame:
					return
				
				scene.update(events, 1 / 30.0)
				
				if scene != scene.next:
					old = scene
					scene = scene.next
					old.next = None
				
				scene.render()
				
				Q.clockTick()
			
	
	def toggleFullScreen(self):
		if self.isPyglet:
			print("Full screen not supported in pyglet version yet.")
		else:
			if self.isFullScreen:
				self.screen = self.pygame.display.set_mode((width, height))
			else:
				self.screen = self.pygame.display.set_mode((width, height), self.pygame.FULLSCREEN)
		self.isFullScreen = not self.isFullScreen
	
	def quit(self):
		self.exitGame = True
	
	def pumpEvents(self):
		
		events = []
		
		if self.isPyglet:
			pass
		else:
			for event in self.pygame.event.get():
				if event.type == self.pygame.QUIT:
					self.exitGame = True
				
				if event.type == self.pygame.KEYDOWN:
					if event.key == self.pygame.K_F4 and (self.pressedActions['lalt'] or self.pressedActions['ralt']):
						self.exitGame = True
					
					if event.key == self.pygame.K_p:
						self.toggleFullScreen()
						
				if event.type == self.pygame.KEYUP or event.type == self.pygame.KEYDOWN:
					action = self._ACTION_BY_PYGAME_EVENT.get(event.key)
					if action != None:
						down = event.type == self.pygame.KEYDOWN
						self.pressedActions[action] = down
						events.append(Action(action, down))
				
		return events
	
	def setScreenAlpha(self, value):
		if value < 0: value = 0
		if value > 1: value = 1
		self.screenAlpha = value
	
	def clockTick(self):
		if self.isPyglet:
			pass
		else:
			alpha = int(self.screenAlpha * 255 + .5)
			if alpha < 255:
				overlay = self.blackener
				if overlay == None:
					overlay = self.screen.convert()
					self.blackener = overlay
				overlay.set_alpha(255 - alpha)
				self.screen.blit(overlay, (0, 0))
				
			self.pygame.display.flip()
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
		if self.isPyglet:
			pass
		else:
			self.screen.fill((r, g, b))
	
	def drawImageInstance(self, img, x, y):
		if self.isPyglet:
			pass
		else:
			self.screen.blit(img, (x, y))
	
	def drawImageTopLeft(self, path, x, y):
		if self.isPyglet:
			pass
		else:
			self.screen.blit(IMAGES.get(path), (x, y))
	
	def drawImage(self, path, x, y, angle = None):
		if self.isPyglet:
			pass
		else:
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

pygm = None
pygl = None
try:
	import pyglet
	pygl = pyglet
except:
	pass

try:
	import pygame
	pygm = pygame
except:
	pass

Q = Engine(pygm, pygl)

