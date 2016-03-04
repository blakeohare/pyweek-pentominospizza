# Action types: up, down, left, right, space, enter


class Action:
	def __init__(self, type, down, coord = None):
		self.type = type
		self.down = down
		self.up = not down
		self.coord = coord

class Engine:
	def __init__(self, pyglet):
		self.pyglet = pyglet
		outerSelf = self
		self.fontEngine = None
		
		class PygletWindow(pyglet.window.Window):
			def __init__(self, width, height, title):
				pyglet.window.Window.__init__(self, width, height, title)
			
			def on_draw(self):
				outerSelf.pygletOnDraw(self)
			
			def on_key_press(self, symbol, modifiers):
				outerSelf.pygletKeyEvent(symbol, True)
			
			def on_key_release(self, symbol, modifiers):
				outerSelf.pygletKeyEvent(symbol, False)
			
			def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
				outerSelf.pygletMouseMove(x, y)
			
			def on_mouse_press(self, x, y, button, modifiers):
				outerSelf.pygletMouseClick(x, y, button == pyglet.window.mouse.LEFT, True)
			
			def on_mouse_release(self, x, y, button, modifiers):
				outerSelf.pygletMouseClick(x, y, button == pyglet.window.mouse.LEFT, False)
				
				
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
		self.mouseX = 0
		self.mouseY = 0
		self.pygletEvents = []
		self.pygletThings = []
		for type in 'up down left right space enter f4'.split(' '):
			self.pressedActions[type] = False
	
	def pygletMouseMove(self, x, y):
		self.mouseX = x
		self.mouseY = y
		self.pygletEvents.append(Action('mousemove', None, (x, 600 - y)))
	
	def pygletMouseClick(self, x, y, left, down):
		self.mouseX = x
		self.mouseY = y
		self.pygletEvents.append(Action('mouseleft' if left else 'mouseright', down, (x, 600 - y)))
		
	
	def pygletKeyEvent(self, symbol, isDown):
		key = self._ACTION_BY_PYGLET_EVENT.get(symbol)
		if key != None:
			self.pygletEvents.append(Action(key, isDown))
			self.pressedActions[key] = isDown
		
	def renderText(self, text, size, x, y):
		obj = GfxText(text, size, x, y)
		self.pygletThings.append(obj)
		return obj
	
	def pygletOnDraw(self, window):
		window.clear()
		self.scene.render()
		
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
	
		self.window = self.windowClass(width, height, title)
		self.scene = scene
		self.pyglet.clock.schedule_interval(self.pygletUpdate, 1 / 60.0) # faster than the canonical SPF
		
		self.pyglet.resource.path = ['./source']
		self.pyglet.resource.reindex()
		self.pyglet.app.run()
	
			
	
	def toggleFullScreen(self):
		print("Full screen not supported in pyglet version yet.")
		self.isFullScreen = not self.isFullScreen
	
	def quit(self):
		self.exitGame = True
	
	def pumpEvents(self):
		
		events = []
		
		return events
	
	def setScreenAlpha(self, value):
		if value < 0: value = 0
		if value > 1: value = 1
		self.screenAlpha = value
	
	def clockTick(self):
		pass
	
	def fill(self, r, g, b):
		pass # Not used, actually.
	
	def drawImageInstance(self, img, x, y):
		pass # not used
	
	def drawImageTopLeft(self, path, x, y):
		return GfxImage(img, x, y)
	
	def drawImage(self, path, x, y, angle = None):
		pass
	
	def drawImageWithRotationalOffset(self, path, x, y, radius, angle):
		pass

try:
	import pyglet
	Q = Engine(pyglet)
except:
	print("Pyglet is required to play: https://bitbucket.org/pyglet/pyglet/wiki/Home")
	os.sys.exit(0)
	

