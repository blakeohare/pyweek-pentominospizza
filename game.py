import math
import time
import random
import os

PI = 3.14159265358979323
TWO_PI = PI * 2
HALF_PI = PI / 2

# FPS and Seconds per frame
# ...at least canonically at 30 FPS which must of the calculations are done in due 
# to writing in PyGame initially. Divide/multiply the dt value by these.
FPS = 30.0
SPF = 1.0 / FPS

EDITOR_ENABLED = True
#EDITOR_ENABLED = False



class ActiveSession:
	def __init__(self):
		self.startTime = 0
		self.id = None
	
	def startGame(self, id, timeLimitSeconds):
		self.id = id
		self.timeLimitSeconds = timeLimitSeconds
		self.startTime = time.time()
		self.longestJump = 0.0
		self.currentJump = None
		self.jumpCount = 0
		self.isJumpRecord = False
		self.lastKnownJumpRecord = DB.getFloat(id + '_longestjump')
		self.timerRunning = True
		self.timeAccrued = 0.0
	
	def startJump(self):
		self.jumpCount += 1
		self.currentJump = self.getCurrentTime()
		self.isJumpRecord = False
	
	def ensureTimerRunning(self, toggle):
		if toggle == self.timerRunning:
			return
		
		self.timerRunning = toggle
		if toggle:
			self.startTime = time.time() - self.timeAccrued
		else:
			self.timeAccrued = time.time() - self.startTime
	
	def getCurrentTime(self):
		if self.timerRunning:
			return time.time() - self.startTime
		else:
			return self.timeAccrued
	
	def endJump(self):
		jumpDuration = self.getCurrentTime() - self.currentJump
		if jumpDuration > self.longestJump:
			self.longestJump = jumpDuration
		if jumpDuration > self.lastKnownJumpRecord:
			self.isJumpRecord = True
			self.lastKnownJumpRecord = jumpDuration
		self.currentJump = None
	
	def popJumpRecordStatus(self):
		if self.isJumpRecord:
			self.isJumpRecord = False
			return True
		return False
	
	def getCurrentJump(self):
		if self.currentJump == None:
			return None
		return self.getCurrentTime() - self.currentJump
	
	def getLongestJump(self):
		return self.longestJump
	
	def endGame(self):
		self.gameDuration = time.time() - self.startTime
		
	

ACTIVE_SESSION = ActiveSession()





class CreditsScene:
	def __init__(self):
		self.next = self
		self.things = {}
		self.counter = 0
	
	def update(self, events, dt):
		self.counter += dt
		
		for event in events:
			if event.down and event.type in ('space', 'enter'):
				self.next = TransitionScene(self, TitleScene())
	
	
	def render(self):
		bg = self.things.get('bg')
		if bg == None:
			bg = GfxImage('background/space1.png')
			self.things['bg'] = bg
		
		bg.blitSimple(0, 0)
		
		self.getText('Programming', 'S', 80, 200).render()
		self.getText("Blake O'Hare", 'L', 80, 260).render()
		
		self.getText('Art', 'S', 370, 200).render()
		self.getText('Sophia Baldonado', 'L', 370, 260).render()
		
		y = 450
		self.getText('Press ENTER or something', 'S', 300, y - abs(int(math.sin(self.counter * TWO_PI) * 15))).render()
		
	
	def getText(self, text, size, x, y):
		t = self.things.get(text)
		if t == None:
			t = Q.renderText(text, size, x, y)
			self.things[text] = t
		else:
			t.setPosition(x, y)
		return t




class CutScene:
	def __init__(self):
		self.next = self
		self.stub = None
		self.index = 0
		self.state_counter = 0.0
		self.progress = 0.0
		
		self.states = [
			('start', 2),
			('ringring', 1),
			('phone1-normal', 2),
			('ufo-enter', 1),
			('ufo-wait', 1),
			('ufo-blast', 1),
			('white-in', 1),
			('white', 1),
			('white-out', 1),
			('end', 2),
		]

		self.images = {}

	def render(self):
		if self.index >= len(self.states):
			state = self.states[-1]
		else:
			state = self.states[self.index]

		progress = self.state_counter / state[1]
		if progress < 0: progress = 0.0
		elif progress > 1: progress = 1.0
		antiprogress = 1.0 - progress
		id = state[0]

		asteroidsY = math.sin(time.time() * TWO_PI) * 4
		
		if id == 'start':
			self.blitImage('window-background-small', 350, 50)
			self.blitImage('page1', 0, 0)
		elif id == 'ringring':
			self.blitImage('window-background-small', 350, 50)
			self.blitImage('page1', 0, 0)
			self.drawText("*RING RING*", 566, 31)
		elif id == 'phone1-normal':
			self.blitImage('window-background', 85, 58)
			self.blitImage('window', 0, 0)
		elif id == 'ufo-enter':
			self.blitImage('window-background', 85, 58)
			yStart = -300
			yEnd = 100
			y = progress * yEnd + antiprogress * yStart
			self.blitImage('ufo', 200, y)
			self.blitImage('window', 0, 0)
		elif id == 'ufo-wait':
			self.blitImage('window-background', 85, 58)
			self.blitImage('ufo', 200, 100)
			self.blitImage('window', 0, 0)
		elif id == 'ufo-blast':
			self.blitImage('window-background', 85, 58)
			self.blitImage('beam', 270, 180)
			self.blitImage('ufo', 200, 100)
			self.blitImage('window', 0, 0)
		elif id == 'white-in':
			self.blitImage('window-background', 85, 58)
			self.blitImage('beam', 270, 180)
			self.blitImage('ufo', 200, 100)
			self.blitImage('window', 0, 0)
			self.blitImage('white', 0, 0, progress)
		elif id == 'white':
			self.blitImage('white', 0, 0, 1.0)
		elif id == 'white-out':
			
			self.blitImage('space-background', 85, 58)
			self.blitImage('space-asteroids', 85, 58 + asteroidsY)
			self.blitImage('window', 0, 0)
			self.blitImage('white', 0, 0, antiprogress)
		elif id == 'end':
			self.blitImage('space-background', 85, 58)
			self.blitImage('space-asteroids', 85, 58 + asteroidsY)
			self.blitImage('window', 0, 0)

	def update(self, events, dt):
		self.state_counter += dt
		if self.index >= len(self.states):
			self.leave()

		for event in events:
			if event.down and (event.type == 'enter' or event.type == 'space'):
				self.leave()

		if self.index >= len(self.states):
			self.index = len(self.states) - 1

		state = self.states[self.index]

		total = state[1]
		if self.state_counter >= total:
			self.state_counter = 0
			self.index += 1

		self.progress = 1.0 * self.state_counter / total

	def leave(self):
		self.next = TransitionScene(self, TitleScene())
		DB.setValue('intro_shown', True)
		DB.save()

	def drawText(self, text, x, y):
		txt = self.images.get('T:' + text)
		if txt == None:
			txt = Q.renderText(text, 'L', x, y)
			self.images['T:' + text] = txt

		txt.render()

	def blitImage(self, path, x, y, opacityRatio = None):
		img = self.images.get(path)
		if img == None:
			img = GfxImage('cutscene/' + path + '.png')
			self.images[path] = img

		if (opacityRatio != None):
			alpha = int(opacityRatio * 255)
			if alpha < 0: alpha = 0
			if alpha > 255: alpha = 255
			img.sprite.opacity = alpha

		img.blitSimple(x, y)





_DEBRIS_OFFSETS = (
	(0, 0),
	(1, 0),
	(0, 1),
	(1, 1),
)

class Debris:
	def __init__(self, x, y, type):
		self.x = x
		self.y = y
		self.type = type
		self.theta = random.random() * TWO_PI
		self.img = GfxImage('rocks/' + type + '.png')
		self.angularVelocity = random.random() / 25.0
	
	def update(self, scene, dt):
		self.theta += self.angularVelocity * (dt * FPS)
	
	def render(self, cx, cy):
		x = (self.x + cx * .6) % 1000 - 500
		y = (self.y + cy * .6) % 1000 - 500
		
		for offset in _DEBRIS_OFFSETS:
			ox, oy = offset
			self.img.blitRotation(x + ox * 1000, y + oy * 1000, self.theta)





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
		#self.eventLoop = pyglet.app.EventLoop()
		self.fader = None
		
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
			pyglet.window.key.A: 'left',
			pyglet.window.key.S: 'down',
			pyglet.window.key.W: 'up',
			pyglet.window.key.D: 'right',
			pyglet.window.key.Y: 'save',
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
		if self.screenAlpha != 1:
			if self.fader == None:
				self.fader = GfxImage('just_black.png')
				self.fader.setSize(800, 600)
			self.fader.setOpacity(255 * (1.0 - self.screenAlpha))
			self.fader.blitSimple(0, 0)
		
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
		self.eventLoop.exit()
	
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
	






FONTS_SIZE_BY_TSHIRT = {
	'XL': 36,
	'L': 20,
	'M': 16,
	'S': 12,
}

LETTERS = 'abcdefghijklmnopqrstuvwxyz'
LETTERS += LETTERS.upper()
LETTERS += '0123456789'
LETTERS += '!@#$%^&*`~()-_=+[]{}|\\;:\'",.<>?/'

class PyGameFontEngine:
	def __init__(self):
		self.characters_by_size = {}
	

	def render(self, text, size, x, y):
		size_set = self.characters_by_size.get(size)
		if size_set == None:
			size_set = {}
			font = pygame.font.Font('source' + os.sep + 'fonts' + os.sep + 'orena.ttf', FONTS_SIZE_BY_TSHIRT[size.upper()])
			for letter in LETTERS:
				size_set[letter] = font.render(letter, True, (255, 255, 255))
			self.characters_by_size[size] = size_set
		
		for c in text:
			if c == ' ':
				x += size_set['v'].get_width()
			else:
				letter = size_set.get(c, '?')
				Q.drawImageInstance(letter, x, y)
				x += letter.get_width()
				





_GFX_IMAGE_LIBRARY = {}

class RawImage:
	def __init__(self, resource):
		self.resource = resource
		# original width and height
		self.width = resource.width
		self.height = resource.height
		self.cx = self.width // 2
		self.cy = self.height // 2
		self.centered = False
		self.anchor_x = 0
		self.anchor_y = 0
	
	def anchorTopLeft(self):
		if self.centered:
			self.centered = False
			self.resource.anchor_x = 0
			self.resource.anchor_y = 0
	
	def anchorCenter(self):
		if not self.centered:
			self.centered = True
			self.resource.anchor_x = self.cx
			self.resource.anchor_y = self.cy


class GfxImage:
	def __init__(self, path):
		img = _GFX_IMAGE_LIBRARY.get(path)
		if img == None:
			img = RawImage(Q.pyglet.resource.image(os.path.join('images', path.replace('/', os.sep)).replace('\\', '/')))
			_GFX_IMAGE_LIBRARY[path] = img
		self.img = img
		self.sprite = Q.pyglet.sprite.Sprite(img.resource)
		self.centered = False
		self.sprite.anchor_x = 0
		self.sprite.anchor_y = 0
		self.width = img.width
		self.height = img.height
		self.theta = None
		
	def setOpacity(self, ratio):
		self.sprite.opacity = ratio
	
	def setSize(self, width, height):
		self.width = width
		self.height = height
		self.sprite.image.width = width
		self.sprite.image.height = height
		self.centered = False
		self.sprite.anchor_x = 0
		self.sprite.anchor_y = 0
		self.img.cx = width / 2.0
		self.img.cy = height / 2.0
		
	def blitSimple(self, x, y):
		self.img.anchorTopLeft()
		if self.theta != None:
			self.sprite.rotation = 0
			self.theta = None
		self.sprite.x = x
		self.sprite.y = Q.height - y - self.height
		if self.centered:
			self.centered = False
			self.sprite.anchor_x = 0
			self.sprite.anchor_y = 0
		
		self.sprite.draw()
	
	def blitRotation(self, x, y, theta):
		self.img.anchorCenter()
		if self.theta == None: self.theta = 0
		diff = theta - self.theta
		if diff < -0.00001 or diff > 0.00001:
			self.theta = theta
			self.sprite.rotation = 360 / TWO_PI * theta + 90
		
		ry = Q.height - y
		
		self.sprite.set_position(x, ry)
		self.sprite.draw()	
	




class GfxText:
	def __init__(self, text, size, x, y):
		self.text = text
		self.size = size
		self.x = x
		self.y = y
		self.label = None
		self.dead = False
		self.obj = None
		self.invalid = True
	
	def render(self):
		if self.invalid:
			size = Q._FONT_SIZE_BY_SHIRT[self.size]
			y = self.y - size
			self.obj = Q.pyglet.text.Label(self.text, font_name = 'Arial', font_size = size, x = self.x, y = Q.height - y, anchor_x = 'left', anchor_y = 'top')
			self.invalid = False
		self.obj.draw()
	
	def setPosition(self, x, y):
		if self.x != x or self.y != y:
			self.x = x
			self.y = y
			self.invalid = True





GRAVITY_ID_ALLOC = [0]

def getIdFromBody(body):
	if body == None: return None
	return body.id

def getBodyFromId(id, bodies):
	if id == None: return None
	return bodies.get(id)
	
class GravityBody:
	def __init__(self, type, x, y, radius, imagePath, rps, rotRat, typeFlag = None):
		# IF YOU ADD ANYTHING HERE, ADD IT TO SAVE AND RESTORE STATE
		self.type = type
		self.id = GRAVITY_ID_ALLOC[0]
		GRAVITY_ID_ALLOC[0] += 1
		self.x = x + 0.0
		self.y = y + 0.0
		self.radius = radius
		self.rotRat = rotRat
		self.image = GfxImage(imagePath)
		self.theta = random.random() * TWO_PI
		self.rps = rps
		self.isDeathy = False
		self.gravity = radius / 100.0
		if self.type == 'blackhole':
			self.gravity *= 4
			self.isDeathy = True
		self.isWater = False
		self.isVolcano = False
		imgWH = (radius * 2, radius * 2)
		if typeFlag == 'water':
			self.isWater = True
		elif typeFlag == 'volcano':
			self.isVolcano = True
			imgWH = (radius * 2.6, radius * 2.6)
		elif typeFlag == 'lava':
			self.isDeathy = True
		elif self.type == 'blackhole':
			imgWH = (radius * 5, radius * 5)
		
		if EDITOR_ENABLED:
			self.isDeathy = False
		
		self.image.setSize(imgWH[0], imgWH[1])
		self.lavaball = None
		if self.type == 'volcano':
			self.lavaball = LavaBall(self)
	
	def update(self, scene, dt):
		self.theta += TWO_PI * self.rps * dt
	
	def render(self, cx, cy):
		self.image.blitRotation(self.x + cx, self.y + cy, self.theta)

	def saveState(self):
		return [self.x, self.y, self.radius, self.image, self.theta, self.rps, self.gravity, self.isWater, self.isVolcano, self.id, self.isDeathy, self.type, self.rotRat]
		
	def restoreState(self, state):
		self.x = state[0]
		self.y = state[1]
		self.radius = state[2]
		self.image = state[3]
		self.theta = state[4]
		self.rps = state[5]
		self.gravity = state[6]
		self.isWater = state[7]
		self.isVolcano = state[8]
		self.id = state[9]
		self.isDeathy = state[10]
		self.type = state[11]
		self.rotRat = state[12]




LAVA_EXIT_VELOCITY = 150 # pixels / sec

class LavaBall:
	def __init__(self, volcano):
		self.body = volcano
		self.x = self.body.x
		self.y = self.body.y
		self.path = None
		self.lifetime = 0
		self.images = [GfxImage('rocks/lavasplash1.png'), GfxImage('rocks/lavasplash2.png')]
		self.image = self.images[0]
	
	def update(self, scene, dt):
		
		if self.path == None:
			theta = int(random.random() * 3) * TWO_PI / 3 + PI / 2 + 8 - .07
			theta += self.body.theta
			self.lifetime = 0
			self.path = theta
			self.image = random.choice(self.images)
		
		self.lifetime += dt
		
		r = self.body.radius + self.lifetime * LAVA_EXIT_VELOCITY
		
		self.x = math.cos(self.path) * r + self.body.x
		self.y = math.sin(self.path) * r + self.body.y
		
		if r - self.body.radius > 300:
			self.path = None
	
	def render(self, cx, cy):
		self.image.blitRotation(self.x + cx, self.y + cy, self.lifetime * 2)




class Level:
	def __init__(self, id):
		self.id = id
		objects = []
		path = os.path.join('source', 'levels', id + '.txt')
		c = open(path, 'rt')
		lines = c.read().split('\n')
		c.close()
		activeObject = None
		for line in lines:
			line = line.strip()
			speedRatio = 1.0
			if len(line) > 0:
				if line[0] != '+':
					parts = line.split(',')
					objectId = parts[0].strip()
					x = int(parts[1].strip())
					y = int(parts[2].strip())
					if len(parts) > 3:
						speedRatio = float(parts[3].strip()) # can be negative to rotate in other direction
					activeObject = (objectId, x, y, [], speedRatio)
					objects.append(activeObject)
				else:
					parts = line[1:].split(',')
					spriteId = parts[0].strip()
					theta = int(parts[1].strip()[1:]) * TWO_PI  / 360
					
					activeObject[3].append((spriteId, theta))
		
		self.stuff = objects

# This is pretty cheesy. Since you can't add or delete asteroids in the editor or change their 
# order, take the bodies and just re-allocate them into the file. This will preserve sprite starting locations.
def saveLevel(playscene):
	bodies = playscene.bodies[:]
	path = os.path.join('source', 'levels', playscene.id + '.txt')
	c = open(path, 'rt')
	lines = c.read().split('\n')
	c.close()
	for i in range(len(lines)):
		line = lines[i].strip()
		if len(line) > 0:
			if line[0] != '+' and len(bodies) > 0:
				body = bodies[0]
				newLine = body.type + ', ' + str(int(body.x)) + ', ' + str(int(body.y)) + ', ' + str(body.rotRat)
				lines[i] = newLine
				bodies = bodies[1:]
	c = open(path, 'wt')
	c.write('\n'.join(lines))
	c.close()
	




class MapMetadata:
	def __init__(self, key, name):
		self.key = key
		self.name = name
		self.next = None
		
class MapDatabase:
	def __init__(self):
		self.values = {}
		self.order = []
		
		c = open(os.path.join('source', 'levels', 'manifest.txt'), 'rt')
		lines = c.read().split('\n')
		c.close()
		
		prev = None
		for line in lines:
			parts = line.split(':')
			if len(parts) == 2:
				key = parts[0].strip()
				name = parts[1].strip()
				metadata = MapMetadata(key, name)
				metadata.prev = prev
				if prev != None:
					prev.next = metadata
				prev = metadata
		
				self.order.append(key)
				self.values[key] = metadata
	
	def get(self, key):
		return self.values.get(key)
	
	def getKeys(self):
		return self.order[:]
	
	def isUnlocked(self, key):
		if self.order[0] == key: return True
		m = self.get(key)
		if m == None: return False
		key = m.prev.key
		return DB.getBoolean(key + '_completed')

MAP_DB = MapDatabase()




MAP_COLUMN_SPACING = [280, 100, 120, 120, 120, 120]

class MapSelectScreen:
	def __init__(self):
		self.next = self
		
		self.index = 1
		self.counter = 0
		self.bg = None
		self.cursor = None
		
		self.options = []
		
		self.options.append([
			'BACK',
			20,
			[None],
			['Back to title screen'],
			])
		
		ch = ['Attempts', 'Fastest Time', 'Fewest Jumps', 'Longest Jump']
		self.columnHeaders = [
			[None] * len(ch), # text labels
			ch]
		
		self.index = 0
		for key in MAP_DB.getKeys():
			if ACTIVE_SESSION.id == key:
				self.index = len(self.options)
			m = MAP_DB.get(key)
			unlocked = MAP_DB.isUnlocked(m.key)
			fastestTime = None
			longestJump = None
			fewestJumps = None
			timesPlayed = None
			
			title = '(Not unlocked yet)'
			
			if unlocked:
				title = m.name
				if DB.hasValue(key + '_fastesttime'):
					fastestTime = DB.getFloat(key + '_fastesttime')
				if DB.hasValue(key + '_longestjump'):
					longestJump = DB.getFloat(key + '_longestjump')
				if DB.hasValue(key + '_fewestjumps'):
					fewestJumps = DB.getInt(key + '_fewestjumps')
				timesPlayed = DB.getInt(key + '_timesplayed')
			
			option = [
				title,
				nstr(timesPlayed),
				formatTime(fastestTime),
				nstr(fewestJumps),
				formatTime(longestJump),
			]
			
			option = [key, 0, [None] * len(option), option] # [0] -> map key, [1] -> bottom padding, [2] -> pyglet label objects, [3] -> raw string values or None if not present
			
			self.options.append(option)
		self.index += 1
		if self.index >= len(self.options):
			self.index = len(self.options) - 1
	
	def update(self, events, dt):
		self.counter += dt * 30
		confirm = False
		for event in events:
			if event.down:
				if event.type == 'up':
					self.index -= 1
				elif event.type == 'down':
					self.index += 1
				elif event.type == 'space' or event.type == 'enter':
					confirm = True
		
		if self.index < 0:
			self.index = 0
		if self.index >= len(self.options):
			self.index = len(self.options) - 1
		
		if confirm:
			key = self.options[self.index][0]
			if key == 'BACK':
				self.next = TransitionScene(self, TitleScene())
			else:
				timelimit = 3 * 60
				if EDITOR_ENABLED:
					timelimit = 100 * 60
				ACTIVE_SESSION.startGame(key, timelimit)
				self.next = TransitionScene(self, PlayScene('M', key))
		
		
	def render(self):
		if self.bg == None:
			self.bg = GfxImage('background/space1.png')
		self.bg.blitSimple(0, 0)
		
		
		y = 40
		index = -1
		for option in self.options:
			index += 1
			x = 60
			
			if index == 1:
				xSave = x
				x += MAP_COLUMN_SPACING[0]
				for colIndex in range(len(self.columnHeaders[0])):
					img = self.columnHeaders[0][colIndex]
					if img == None:
						img = Q.renderText(self.columnHeaders[1][colIndex], 'S', x, y - 40)
						self.columnHeaders[0][colIndex] = img
					x += MAP_COLUMN_SPACING[colIndex + 1]
					img.render()
			
				x = xSave
			if index == self.index:
				# needs to be adjusted to dt
				yOffset = int(abs(math.sin(self.counter * TWO_PI / FPS) * 16))
				if self.cursor == None:
					self.cursor = GfxImage('menus/pizza.png')
				cx = x - 50
				cy = y - yOffset - 30
				self.cursor.blitSimple(cx, cy)
				
			yPad = option[1]
			buttons = option[2]
			text = option[3]
			
			for i in range(len(buttons)):
				button = buttons[i]
				if button == None and text[i] != None:
					button = Q.renderText(text[i], 'M', x, y)
					buttons[i] = button
				x += MAP_COLUMN_SPACING[i]
				
				if button != None:
					button.render()
			
			y += 50 + yPad
		
			




class OptionsMenu:
	def __init__(self):
		self.next = self
		self.index = 0
		self.images = {}
		
	
	def update(self, events, dt):
		enter = False
		for event in events:
			if event.down:
				if event.type == 'up':
					self.index -= 1
				elif event.type == 'down':
					self.index += 1
				elif event.type in ('space', 'enter'):
					enter = True
		if self.index < 0: self.index = 0
		elif self.index > 1: self.index = 1
		
		if enter:
			if self.index == 0:
				DB.setValue('magic', not DB.getBoolean('magic'))
				DB.save()
			else:
				self.next = TransitionScene(self, TitleScene())
	
	def render(self):
		self.getImage('background/space1.png').blitSimple(0, 0)
		options = ['Magic', 'Back to Title Screen']
		if not DB.getBoolean('magic'):
			options[0] = 'More Magic'
		y = 300
		for i in range(2):
			x = 200
			self.getText(options[i], x, y).render()
			if i == self.index:
				yOffset = abs(math.sin(time.time() * 2 * 3.14159)) * 15
				x -= 70
				self.getImage('menus/pizza.png').blitSimple(x, y - 25 - yOffset)
			y += 100
	
	def getText(self, text, x, y):
		key = 'K:' + text
		img = self.images.get(key)
		if img == None:
			img = Q.renderText(text, 'L', x, y)
			self.images[key] = img
		return img
		
	
	def getImage(self, path):
		img = self.images.get(path)
		if img == None:
			img = GfxImage(path)
			self.images[path] = img
		return img




class PauseScreen:

	def __init__(self, bg):
		self.counter = 0
		self.next = self
		self.bg = bg
		self.overlay = GfxImage('dark_overlay.png')
		self.overlay.setSize(800, 600)
		self.index = 0
		
		x = 200
		y = 250
		margin = 100
		self.options = [
			Q.renderText('Resume', 'L', x, y),
			Q.renderText('Restart', 'L', x, y + margin),
			Q.renderText('Back to Menu', 'L', x, y + margin * 2),
		]
		
		self.cursor = GfxImage('menus/pizza.png')
	
	def update(self, events, dt):
		self.counter += dt
		ACTIVE_SESSION.ensureTimerRunning(False)
		confirm = False
		for event in events:
			if event.down:
				if event.type == 'space' or event.type == 'enter':
					confirm = True
				elif event.type == 'up':
					self.index -= 1
				elif event.type == 'down':
					self.index += 1
		if self.index < 0:
			self.index = 0
		if self.index > 2:
			self.index = 2
		
		if confirm:
			if self.index == 0:
				self.next = self.bg
				self.next.next = self.next
			elif self.index == 1:
				self.next = TransitionScene(self, ['M', self.bg.id])
			elif self.index == 2:
				self.next = TransitionScene(self, MapSelectScreen())
					
		
	
	def render(self):
		self.bg.render()
		self.overlay.blitSimple(0, 0)
		
		for option in self.options:
			option.render()
		
		x = 50
		y = 250 + 100 * self.index - abs(15 * math.sin(self.counter * TWO_PI))
		
		self.cursor.blitSimple(x, y)
		
		




'''
data saved:
boolean -> intro_shown

boolean -> {map key}_completed
float -> {map_key}_longestjump (seconds)
float -> {map_key}_fastesttime (seconds)
int -> {map_key}_fewestjumps
int -> {map_key}_timesplayed

A map is considered unlocked if it is first in the manifest or its previous map is marked as _completed

'''

INT = type(42)
FLOAT = type(42.5)
STRING = type('42')
BOOL = type(True)
LIST = type([])

class PersistentData:
	def __init__(self):
		self.values = {}
		self.folder = '.'
		self.filename = 'pp_save_data.txt'
		self.initialize() # sets the save file or doesn't if it can't figure out the system.
	
	def initialize(self):
		if os.name == 'nt':
			appdata = os.environ.get('APPDATA')
			if appdata != None:
				self.folder = os.path.join(appdata, 'PentominosPizza')
		elif os.sys.platform.startswith('linux') or os.name == 'os2':
			if os.path.exists('~') and os.path.isdir('~'):
				self.folder = os.path.join('~', '.pentominospizza')
		else:
			pass # just leave as '.'
		
		if self.folder != '.' and not os.path.exists(self.folder):
			try:
				os.makedirs(self.folder)
			except:
				print("persistent file creation failed")
				self.folder = '.'
				self.initialize()
				return
		
		path = os.path.join(self.folder, self.filename)
		data = ''
		if os.path.exists(path):
			try:
				c = open(path, 'rt')
				data = c.read()
				c.close()
			except:
				data = ''
		
		for line in data.split('\n'):
			line = line.strip()
			if len(line) > 0:
				parts = line.split(':')
				if len(parts) >= 3:
					t = parts[0].upper().strip()
					k = parts[1].strip()
					v = ':'.join(parts[2:]).strip()
					if t == 'I':
						try:
							v = int(v)
						except:
							k = None
					elif t == 'F':
						try:
							v = float(v)
						except:
							k = None
					elif t == 'B':
						v = v == '1'
					elif t == 'S':
						pass
					elif t == 'N':
						v = None
					else:
						k = None
					if k != None:
						self.values[k] = v
	
	def save(self):
		if self.folder == None: return
		output = []
		for key in self.values.keys():
			t = None
			value = self.values[key]
			ktype = type(value)
			if ktype == INT:
				t = 'I'
			elif ktype == STRING:
				t = 'S'
			elif ktype == BOOL:
				t = 'B'
				value = 1 if value else 0
			elif ktype == FLOAT:
				t = 'F'
			elif value == None:
				t = 'N'
				value = '-'
			output.append(t + ':' + key + ':' + str(value))
		
		try:
			c = open(os.path.join(self.folder, self.filename), 'wt')
			c.write('\n'.join(output))
			c.close()
		except:
			print("Persistent file write failed.")
			pass
	
	def getBoolean(self, key, default = False):
		return self.values.get(key, default) == True
	
	def getFloat(self, key, default = 0.0):
		output = self.values.get(key, default)
		if type(output) == FLOAT:
			return output
		if type(output) == INT:
			return output + 0.0
		return default
	
	def getInteger(self, key, default = 0):
		return self.getInt(key, default)
	
	def getInt(self, key, default = 0):
		output = self.values.get(key, default)
		if type(output) == INT:
			return output
		if type(output) == FLOAT:
			return int(output)
		return default
	
	def getString(self, key, default = None):
		return str(self.values.get(key, default))
	
	def hasValue(self, key):
		return key in self.values
	
	def setValue(self, key, value):
		self.values[key] = value

DB = PersistentData()




_BODY_TYPE_INFO = {
	# image name, radius
	'halfgrass': ('halfgrass', 150),
	'lava': ('lava', 250),
	'lavamini': ('lavamini', 150),
	'rock1': ('rock1', 150),
	'rock2': ('rock2', 150),
	'rock3': ('rock3', 150),
	'rock4': ('rock4', 150),
	'volcano': ('volcano', 150),
	'water': ('water', 150),
	'blackhole': ('blackhole', 80),
}

class PlayScene:
	# Restore type is either 'M' for map or 'S' for state
	# arg is level string ID for M and another playscene for S
	def __init__(self, restoreType, arg):
		self.YOU_DEAD = False
		self.next = self
		self.bg = GfxImage('background/space1.png')
		self.pointer = GfxImage('pointer.png')
		
		self.sprites = []
		self.player = None
		self.bodies = []
		self.sharks = [] # too much different mechanics than sprites, don't want to introduce bugs 3 hours before game is due. adding as a different type.
		self.lavaballs = []
		
		self.hoverTime = None # counter for when you are jumping
		self.recordIndicator = None
		self.countdownLabel = None
		self.timeLeft = None
		self.timeLeftValue = None
		
		self.mouseXY = (0, 0)
		self.mouseBody = None
		self.mouseBodyStartOffset = None # offset from center of body that user clicked
		
		if restoreType == 'M':
			self.level = Level(arg)
			self.id = arg
			for body in self.level.stuff:
				type, x, y, sprites, speedRatio = body
				imgPath, radius = _BODY_TYPE_INFO[type]
				flag = None
				if type == 'water':
					flag = 'water'
				elif type == 'volcano':
					flag = 'volcano'
				elif type == 'lava' or type == 'lavamini':
					flag = 'lava'
				
				body = GravityBody(type, x, y, radius, 'rocks/' + imgPath + '.png', speedRatio / 30.0, speedRatio, flag)
				for sprite in sprites:
					spriteInstance = None
					type, angle = sprite
					if type == 'player':
						self.player = Sprite('player', 'G', body, angle)
					elif type == 'store':
						spriteInstance = Sprite('store', 'G', body, angle)
					elif type in ('house1', 'house2', 'house3'):
						spriteInstance = Sprite(type, 'G', body, angle)
					else:
						print("Unknown sprite type: " + type)
					if spriteInstance != None:
						self.sprites.append(spriteInstance)
				self.bodies.append(body)
			
			if self.player != None:
				# ensure player is rendered last so always on top
				self.sprites.append(self.player)
		elif restoreType == 'S':
			bodiesById = {}
			self.id = arg.id
			for bodyState in arg.savedStateBodies:
				gb = GravityBody('rock1', 0, 0, 150, 'rocks/rock1.png', 0, 0, None) # dummy value
				gb.restoreState(bodyState)
				self.bodies.append(gb)
				bodiesById[gb.id] = gb
			for spriteState in arg.savedStateSprites:
				sprite = Sprite('player', 'R', spriteState, bodiesById)
				if sprite.type == 'player':
					self.player = sprite
				self.sprites.append(sprite)
		
		self.debris = []
		
		for i in range(10):
			self.debris.append(Debris(1000 * random.random(), random.random() * 1000, 'small-debris' + str(int(random.random() * 8) + 1)))
		
		self.cameraTargetX = None
		self.cameraTargetY = None
		self.cameraCurrentX = None
		self.cameraCurrentY = None
		
		# These values are immediately set by saveState() and will never actually be null when the game update phase is running.
		self.savedStateBodies = None
		self.savedStateSprites = None
		
		self.saveState()
		
		for sprite in self.sprites:
			if sprite.type.startswith('house'):
				self.victoryPlanet = sprite.ground
				break
		
		if self.id == 'level5' or self.id == 'level9' or self.id == 'level10':
			for body in self.bodies:
				if body.type == 'water':
					self.sharks.append(Shark(body))
		
		for body in self.bodies:
			if body.lavaball != None:
				self.lavaballs.append(body.lavaball)
	
	def saveState(self):
		mapping = {} # body instance to index in the list
		bodies = []
		sprites = []
		bodyToIndex = {}
		for body in self.bodies:
			bodyToIndex[body] = len(bodies)
			bodies.append(body.saveState())
		
		for sprite in self.sprites:
			sprites.append(sprite.saveState())
		
		self.savedStateBodies = bodies
		self.savedStateSprites = sprites
	
	def update(self, events, dt):
		ACTIVE_SESSION.ensureTimerRunning(True)
		
		if ACTIVE_SESSION.getCurrentTime() > ACTIVE_SESSION.timeLimitSeconds:
			self.triggerLose()
			return
			
		if not self.YOU_DEAD:
			dx = 0
			if Q.pressedActions['left']:
				dx = -1
				self.player.facingLeft = True
			elif Q.pressedActions['right']:
				dx = 1
				self.player.facingLeft = False
			
			self.player.applyWalk(dx)
		
			jump = False
			jumpRelease = False
			for event in events:
				if (event.type == 'space' or event.type == 'up') and event.down:
					jump = True
				elif event.type == 'enter' and event.down:
					self.next = PauseScreen(self)
				elif EDITOR_ENABLED and self.cameraCurrentX != None:
					if event.type == 'save' and event.down:
						saveLevel(self)
					elif event.coord != None:
						x, y = event.coord
						rawXY = (x, y)
						x = self.cameraCurrentX - 400 + x
						y = self.cameraCurrentY - 300 + y
						if event.type == 'mousemove':
							if self.mouseBody != None:
								oldXY = (self.mouseBody.x, self.mouseBody.y)
								self.mouseBody.x = int(x - self.mouseBodyStartOffset[0])
								self.mouseBody.y = int(y - self.mouseBodyStartOffset[1])
								
								
						elif event.type == 'mouseleft':
							if event.down:
								if self.mouseBody == None:
									for body in self.bodies:
										dx = x - body.x
										dy = y - body.y
										if dx ** 2 + dy ** 2 < body.radius ** 2:
											self.mouseBody = body
											self.mouseBodyStartOffset = [dx, dy]
											break
							else:
								if self.mouseBody != None:
									self.mouseBody = None
								
				
			self.player.applyJump(jump, dt)
		
		hb = self.player.getHitBox()
		
		for deb in self.debris:
			deb.update(self, dt)
		for body in self.bodies:
			body.update(self, dt)
		for sprite in self.sprites:
			sprite.update(self, dt)
		for shark in self.sharks:
			shark.update(self, dt)
			dx = shark.x - hb[0]
			dy = shark.y - hb[1]
			if dx ** 2 + dy ** 2 < 17 ** 2:
				if not EDITOR_ENABLED:
					self.triggerDeath()
		for ball in self.lavaballs:
			ball.update(self, dt)
			dx = ball.x - hb[0]
			dy = ball.y - hb[1]
			if dx ** 2 + dy ** 2 < 30 ** 2:
				if not EDITOR_ENABLED:
					self.triggerDeath()
	
	def triggerWin(self):
		self.next = WinScreen(self)
	
	def triggerDeath(self):
		self.YOU_DEAD = True
		self.next = TransitionScene(self, ['S', self])
	
	def triggerLose(self):
		self.next = WinScreen(self, False)
	
	def triggerJumpRecord(self, x, y, amt):
		self.recordIndicator = Q.renderText('New Record! ' + formatTime(amt), 'M', x, y)
		self.recordIndicatorCounters = [x, y, ACTIVE_SESSION.getCurrentTime()]
	
	def render(self):
		tm = ACTIVE_SESSION.getCurrentTime()
		
		self.bg.blitSimple(0, 0)
		
		hb = self.player.getHitBox()
		
		self.cameraTargetX = hb[0]
		self.cameraTargetY = hb[1]
		if self.cameraCurrentX == None:
			self.cameraCurrentX = self.cameraTargetX
			self.cameraCurrentY = self.cameraTargetY
		else:
			self.cameraCurrentX = self.cameraCurrentX * .9 + self.cameraTargetX * .1
			self.cameraCurrentY = self.cameraCurrentY * .9 + self.cameraTargetY * .1
		
		t = int(tm * FPS)
		
		cx = Q.width / 2.0 - self.cameraCurrentX
		cy = Q.height / 2.0 - self.cameraCurrentY
		
		for deb in self.debris:
			deb.render(cx, cy)
		
		for ball in self.lavaballs:
			ball.render(cx, cy)
			
		for body in self.bodies:
			body.render(cx, cy)
		
		for sprite in self.sprites:
			sprite.render(t, cx, cy)
		
		for shark in self.sharks:
			shark.render(cx, cy)
		
		
		if self.recordIndicator != None and self.recordIndicatorCounters != None:
			lifetime = tm - self.recordIndicatorCounters[2]
			if lifetime > 2:
				self.recordIndicatorCounters = None
				self.recordIndicator = None
			else:
				ric = self.recordIndicatorCounters
				self.recordIndicator.setPosition(ric[0] + cx, ric[1] - lifetime * 50 + cy)
				self.recordIndicator.render()
				
		
		vp = self.victoryPlanet
		cx = self.cameraCurrentX
		cy = self.cameraCurrentY
		dx = vp.x - cx
		dy = vp.y - cy
		dist = (dx ** 2 + dy ** 2) ** .5
		if dist > 100:
			ang = math.atan2(dy, dx)
			left = -350
			right = 350
			top = -250
			bottom = 250
			
			for segment in (
				(left, top, right, top),
				(left, top, left, bottom),
				(right, top, right, bottom),
				(left, bottom, right, bottom)
				):
				
				pt = findIntersectionOrNull(ang, segment[0], segment[1], segment[2], segment[3], dist)
				if pt != None:
					self.pointer.blitRotation(pt[0] + 400, pt[1] + 300, ang)
					break
		self.renderTimer()
		
	def renderTimer(self):
		countdown = int(ACTIVE_SESSION.timeLimitSeconds - ACTIVE_SESSION.getCurrentTime() + .99) # +.99 so that when it shows 0 it's the actual deadline
		if countdown < 0: countdown = 0
		timeToShow = formatCountdown(countdown)
		if self.timeLeft == None or self.timeLeftValue != timeToShow:
			self.timeLeft = Q.renderText('Delivery Guarantee: ' + timeToShow, 'L', 400, 50)
		self.timeLeft.render()
			
		
		




class SaveState:
	def __init__(self, playscene):
		self.bodies = []
		self.sprites = []
		
		bodiesToId = {}
		
		for body in playscene.bodies:
			data = [
				body.x,
				body.y,
				body.radius,
				
			]




SHARK_VELOCITY = 2.0

SHARK_IMAGES = [None, None]

class Shark:
	def __init__(self, body):
		self.x = body.x
		self.y = body.y
		self.body = body
		self.target = None
		self.leftFacing = random.random() < .5
		if SHARK_IMAGES[0] == None:
			SHARK_IMAGES[0] = GfxImage('sprites/shark-right.png')
			SHARK_IMAGES[1] = GfxImage('sprites/shark-left.png')
		self.images = SHARK_IMAGES
	
	def update(self, scene, dt):
		player = scene.player
		x = self.body.x
		y = self.body.y
		
		if player.ground == self.body:
			hb = player.getHitBox()
			x = hb[0]
			y = hb[1]
		else:
			if self.target == None:
				theta = random.random()
				x = math.cos(theta) * self.body.radius
				y = math.sin(theta) * self.body.radius
				x += self.body.x
				y += self.body.y
				self.target = (x, y)
			x, y = self.target
			
		dx = x - self.x
		dy = y - self.y
		dist = (dx ** 2 + dy ** 2) ** .5
		if dist > SHARK_VELOCITY * 2:
			ux = dx / dist
			uy = dy / dist
			self.x += SHARK_VELOCITY * ux * dt * FPS
			self.y += SHARK_VELOCITY * uy * dt * FPS
			
			self.leftFacing = dx < 0
		else:
			self.target = None
	
	def render(self, cx, cy):
		img = self.images[self.leftFacing]
		img.blitRotation(self.x + cx, self.y + cy, 0)
		




PLAYER_WALK_VELOCITY = 6.0
PLAYER_JUMP_VELOCITY = 470.0
ASTEROID_GRAVITY_COEFFICIENT = 5000.0 # make bigger for stronger gravity

# If enabled, will skip every other update phase and apply that dt to the next update phase's dt value to ensure that I'm incorporating dt correctly into my calculations
# Be sure to set this to true every once in a while to test.
DT_TEST_ENABLED = False

CACHED_JUMP_TIMES = {} # cache by 10*t

class Sprite:

	def __init__(self, type, startType, x_or_body, y_or_theta_or_bodies_lookup):
		self.r = 10
		self.images = {}
		self.type = type
		self.isPlayer = type == 'player'
		if type == 'player':
			left = []
			right = []
			for i in range(10):
				img = GfxImage('sprites/chet-walk-' + str(i) + '.png')
				img.setSize(img.width // 5, img.height // 5)
				right.append(img)
				img = GfxImage('sprites/chetleft/chet-walk-' + str(i) + '.png')
				img.setSize(img.width // 5, img.height // 5)
				left.append(img)
			self.images['left'] = left
			self.images['right'] = right
		elif type in ('store', 'house1', 'house2', 'house3'):
			self.images['left'] = [GfxImage('sprites/' + type + '.png')]
			self.images['right'] = self.images['left']
		
		self.vx = 0
		self.vy = 0
		self.angularVelocity = 0.0
		self.ground = None
		self.strongestGround = None
		self.thetaFromGround = 0
		self.floatingTheta = 0.0
		self.hitBox = None
		self.facingLeft = False
		self.currentVelocity = (0.0, 0.0)
		self.distanceFromCenter = None
		self.waterJump = 0.0
		self.lastWalk = 0
		
		# for DT_TEST_ENABLED
		self.counter = 0
		self.dt_backlog = 0.0
		
		self.x = None
		self.y = None
		
		if startType == 'R': #restore
			self.restoreState(x_or_body, y_or_theta_or_bodies_lookup)
		elif startType == 'G':
			self.ground = x_or_body
			self.thetaFromGround = y_or_theta_or_bodies_lookup
			if self.ground.isWater:
				print("Starting sprites on water bodies not supported.")
		else:
			self.x = x_or_body + 0.0
			self.y = y_or_theta_or_bodies_lookup + 0.0
	
	def restoreState(self, state, bodiesById):
		self.r = state[0]
		self.type = state[1]
		self.images = state[2]
		self.vx = state[3]
		self.vy = state[4]
		self.angularVelocity = state[5]
		self.ground = getBodyFromId(state[6], bodiesById)
		self.strongestGround = getBodyFromId(state[7], bodiesById)
		self.thetaFromGround = state[8]
		self.floatingTheta = state[9]
		self.hitBox = state[10]
		self.facingLeft = state[11]
		self.currentVelocity = state[12]
		self.distanceFromCenter = state[13]
		self.waterJump = state[14]
		self.counter = state[15]
		self.x = state[16]
		self.y = state[17]
		self.isPlayer = self.type == 'player'
	
	def saveState(self):
		return [
			self.r,
			self.type,
			self.images,
			self.vx,
			self.vy,
			self.angularVelocity,
			getIdFromBody(self.ground),
			getIdFromBody(self.strongestGround),
			self.thetaFromGround,
			self.floatingTheta,
			self.hitBox,
			self.facingLeft,
			self.currentVelocity,
			self.distanceFromCenter,
			self.waterJump,
			self.counter,
			self.x,
			self.y]
	
	def getHitBox(self):
		if self.hitBox == None:
			if self.ground == None:
				self.hitBox = (self.x, self.y, self.r)
			else:
				if self.ground.isWater:
					r = self.distanceFromCenter + self.r
				else:
					r = self.ground.radius + self.r
				x = self.ground.x + r * math.cos(self.thetaFromGround + self.ground.theta)
				y = self.ground.y + r * math.sin(self.thetaFromGround + self.ground.theta)
				self.hitBox = (x, y, self.r)
		return self.hitBox
	
	def applyJump(self, press, dt):
		if press and self.ground != None:
			if self.ground.isWater and self.distanceFromCenter < self.ground.radius:
				self.waterJump = 5
			else:
				ground = self.ground
				jumpVelocity = PLAYER_JUMP_VELOCITY # pixels per second
				r = self.ground.radius + self.r + 5
				theta = self.thetaFromGround + self.ground.theta
				ux = math.cos(theta)
				uy = math.sin(theta)
				
				x = self.ground.x + r * ux
				y = self.ground.y + r * uy
				self.x = x
				self.y = y
				self.vx = ux * jumpVelocity
				self.vy = uy * jumpVelocity
				self.theta = theta
				self.ground = None
				
				if self.isPlayer:
					ACTIVE_SESSION.startJump()
				
				self.vx += self.currentVelocity[0]
				self.vy += self.currentVelocity[1]
			
	
	def applyWalk(self, dir):
		if dir != 0:
			self.lastWalk = time.time()
			self.facingLeft = dir < 0
			v = PLAYER_WALK_VELOCITY
			if self.ground != None:
				# works for both water and solid ground
				self.angularVelocity = v * dir
	
	def updateForFloating(self, scene, dt):
		if DT_TEST_ENABLED:
			self.counter += 1
			if self.counter % 2 == 0:
				self.dt_backlog = dt
				return
			else:
				dt += self.dt_backlog
			
		self.x += self.vx * dt
		self.y += self.vy * dt
		
		gx = 0.0
		gy = 0.0
		strongest_g = -1
		strongest_source = None
		
		for body in scene.bodies:
			dx = body.x - self.x
			dy = body.y - self.y
			dr = self.r + body.radius
			dist = (dx ** 2 + dy ** 2) ** .5
			if dist < 2000:
				if dist <= dr:
					self.ground = body
					
					if self.isPlayer:
						
						ACTIVE_SESSION.endJump()
						if ACTIVE_SESSION.isJumpRecord:
							scene.triggerJumpRecord(self.x, self.y, ACTIVE_SESSION.longestJump)
						
						if body == scene.victoryPlanet:
							scene.triggerWin()
						
					
					self.distanceFromCenter = self.ground.radius + 0.0
					theta = math.atan2(-dy, -dx)
					self.thetaFromGround = theta - body.theta
					if body.isDeathy:
						scene.triggerDeath()
					elif body.isWater:
						pass
					else:
						scene.saveState()
					return
				
			g = body.gravity / (dist / ASTEROID_GRAVITY_COEFFICIENT) ** 2
			
			if g > strongest_g:
				strongest_g = g
				strongest_source = body
			
			ux = dx / dist
			uy = dy / dist
			
			gx += g * ux
			gy += g * uy
		
		self.strongestGround = strongest_source
		if strongest_source != None:
			dx = strongest_source.x - self.x
			dy = strongest_source.y - self.y
			targetTheta = math.atan2(-dy, -dx) % TWO_PI
			currentTheta = self.theta % TWO_PI
			dTheta = currentTheta - targetTheta
			if dTheta > PI:
				currentTheta -= TWO_PI
			if dTheta < -PI:
				targetTheta -= TWO_PI
			
			r = .9 ** (dt * FPS)
			ar = 1.0 - r
			self.theta = r * currentTheta + ar * targetTheta
		
		self.vx += gx * dt
		self.vy += gy * dt
	
	def updateForGround(self, scene, dt):
		v = self.angularVelocity * (dt * FPS)
		if self.ground.isWater:
			self.distanceFromCenter += self.waterJump
			self.waterJump *= .9 ** (dt * FPS)
			
			r = self.distanceFromCenter
			self.distanceFromCenter *= .98 ** (dt * FPS)
			if self.distanceFromCenter < 10:
				self.distanceFromCenter = 10.0
		else:
			r = self.ground.radius
		
		# Law-O-Cosines
		theta = math.acos(((v ** 2) - 2 * (r ** 2)) / (-2 * (r ** 2)))
		if v < 0:
			self.thetaFromGround -= theta
		else:
			self.thetaFromGround += theta
		
		self.angularVelocity *= .8 ** (dt * FPS)
	
	def update(self, scene, dt):
		oldLoc = self.getHitBox()
		if self.ground == None:
			self.updateForFloating(scene, dt)
		else:
			self.updateForGround(scene, dt)
		self.hitBox = None
		newLoc = self.getHitBox()
		
		mx = (newLoc[0] - oldLoc[0]) / dt
		my = (newLoc[1] - oldLoc[1]) / dt
		self.currentVelocity = (mx, my)
		
	def render(self, rc, cx, cy):
		hb = self.getHitBox()
		isWalking = (time.time() - self.lastWalk) < .1
		if not isWalking:
			rc = 1
		else:
			rc = int(rc * 1.3) // 2
		imgs = self.images['left'] if self.facingLeft else self.images['right']
		img = imgs[rc % len(imgs)]
		x = hb[0] + cx
		y = hb[1] + cy
		if self.ground == None:
			img.blitRotation(x, y, self.theta)
		else:
			img.blitRotation(x, y, self.ground.theta + self.thetaFromGround)
		
		if self.isPlayer:
			currentJump = ACTIVE_SESSION.getCurrentJump()
			if currentJump != None and currentJump > 1:
				currentJump = int(currentJump * 10) / 10.0
				key = int(currentJump * 10)
				lbl = CACHED_JUMP_TIMES.get(key)
				x = x - 8
				y = y - 40
				if lbl == None:
					lbl = Q.renderText(formatTime(currentJump), 'M', x, y)
					CACHED_JUMP_TIMES[key] = lbl
				else:
					lbl.setPosition(x, y)
				lbl.render()
				
				
			
		





class TitleScene:
	def __init__(self):
		self.next = self
		self.quit_attempt = False
		self.index = 0
		self.counter = 0
		
		self.cursor = None
		
		self.options = [
			["Play", self.click_play, None],
			["Replay Intro", self.click_intro, None],
			['Options', self.click_options, None],
			['Credits', self.click_credits, None],
			['Exit', self.click_exit, None],
		]
		self.bg = None
		self.textCounter = None
		self.chet = None
		self.title = None
		DB.setValue('views', DB.getInt('views', 0) + 1)
		DB.save()
	
	def update(self, events, dt):
		self.counter += dt * 30
		enter = False
		for event in events:
			if event.down:
				if event.type == 'up':
					self.index -= 1
					self.counter = 0
				elif event.type == 'down':
					self.index += 1
					self.counter = 0
				elif event.type == 'enter' or event.type == 'space':
					enter = True
		
		if self.index < 0: self.index = 0
		if self.index >= len(self.options): self.index = len(self.options) - 1
		
		if enter:
			self.options[self.index][1]()
	
	def click_intro(self):
		self.next = TransitionScene(self, CutScene())
	
	def click_play(self):
		self.next = TransitionScene(self, MapSelectScreen())
	
	def click_options(self):
		self.next = TransitionScene(self, OptionsMenu())
	
	def click_credits(self):
		self.next = TransitionScene(self, CreditsScene())
	
	def click_exit(self):
		# Not sure if this is considered "clean" in Pyglet, but the recommended way didn't seem to work. But it's PyWeek so this is good enough for me.
		os.sys.exit()
	
	def render(self):
		if self.bg == None:
			self.bg = GfxImage('background/space1.png')
			
		self.bg.blitSimple(0, 0)
		
		if self.chet == None:
			self.chet = GfxImage('sprites/chet-walk-1.png')
			r = 1.0 * self.chet.width / self.chet.height
			self.chet.setSize(400 * r, 400)
		self.chet.blitSimple(100, 230)
		
		if self.title == None:
			self.title = GfxImage('menus/title.png')
			self.title.setSize(self.title.width * 1.5, self.title.height * 1.5)
		self.title.blitSimple(10, 0)
		
		x = 480
		y = 100
		i = 0
		for option in self.options:
			text = option[0]
			yOffset = 0
			if i == self.index:
				# needs to be adjusted to dt
				yOffset = int(abs(math.sin(self.counter * TWO_PI / FPS) * 16))
				if self.cursor == None:
					self.cursor = GfxImage('menus/pizza.png')
				self.cursor.blitSimple(x - 70, y - yOffset - 20)
			obj = option[2]
			if obj == None:
				obj = Q.renderText(text, 'XL', x, y)
				option[2] = obj
			obj.setPosition(x, y)
			
			obj.render()
			
			
			
			y += 100
			i += 1
		
	





class TransitionScene:
	def __init__(self, fromScene, toScene):
		self.next = self
		self.fromScene = fromScene
		self.toScene = toScene
		self.duration = FPS
		self.half = self.duration // 2
		self.counter = 0
		self.bg = fromScene
		self.alpha = 0
		
	
	def update(self, events, dt):
		self.counter += dt * FPS
		if self.counter < self.half:
			self.bg = self.fromScene
			progress = 1.0 - 1.0 * self.counter / self.half
		else:
			# Hack alert: don't instantiate a new PlayScene until the old one is done showing.
			if type(self.toScene) == LIST:
				self.toScene = PlayScene(self.toScene[0], self.toScene[1])
			self.bg = self.toScene
			progress = 1.0 * (self.counter - self.half) / self.half
		
		Q.setScreenAlpha(progress)
		
		if self.counter >= self.duration:
			Q.setScreenAlpha(1)
			self.next = self.toScene
		
		self.bg.update(events, dt)
	
	def render(self):
		self.bg.render()





def formatTime(amount):
	if amount == None: return None
	
	deci = int(amount * 100) % 100
	amount = int(amount)
	seconds = amount % 60
	amount = amount // 60
	minutes = amount % 60
	hours = amount // 60
	
	if hours > 0:
		return ':'.join((ensureLength(hours, False), ensureLength(minutes, True), ensureLength(seconds, True) + '.' + ensureLength(deci, True)))
	
	if minutes > 0:
		return ''.join((ensureLength(minutes, False), "' ", ensureLength(seconds, True), '.', ensureLength(deci, True), '"'))
	
	return ensureLength(seconds, False) + "." + ensureLength(deci, True) + '"'

def formatCountdown(seconds):
	minutes = seconds // 60
	seconds = seconds % 60
	if seconds < 10:
		return str(minutes) + ':0' + str(seconds)
	return str(minutes) + ':' + str(seconds)
	
def ensureLength(n, pad):
	if pad and n < 10: return '0' + str(n)
	return str(n)

def nstr(value):
	if value == None: return None
	return str(value)

def safeTan(ang):
	s = math.sin(ang)
	c = math.cos(ang)
	if abs(c) < .00001:
		return 999999999
	return s / c
	
def findIntersectionOrNull(angle, ax, ay, bx, by, dist):
	cx = math.cos(angle) * 500
	cy = math.sin(angle) * 500
	
	if ax == bx :#and abs(cx) * 2 > abs(cy):
		y = safeTan(angle) * abs(ax)
		if ax < 0: y = -y
		if ay > by:
			ay, by = by, ay
		
		if y > ay and y < by:
			if (ax < 0) == (cx < 0):
				if (ax ** 2) + y ** 2 < dist ** 2:
					return (ax, y)
	
	if ay == by :#and abs(cx) > abs(cy) * 2:
		x = abs(ay) / safeTan(angle)
		if ay < 0: x = -x
		if ax > bx:
			ax, by = bx, by
		
		
		
		if x > ax and x < bx:
			if (ay < 0) == (cy < 0):
				if (ay ** 2) + x ** 2 < dist ** 2:
					return (x, ay)
	
	return None





# This is now repurposed for when you lose as well as it needs to apply the record for longest jump

class WinScreen:
	def __init__(self, bg, isWin = True):
		self.next = self
		self.isWin = isWin
		self.bg = bg
		self.overlay = GfxImage('dark_overlay.png')
		self.overlay.setSize(800, 600)
		self.counter = 0
		self.isLongestJumpRecord = False
		id = self.bg.id
		timesPlayed = DB.getInt(id + '_timesplayed') + 1
		DB.setValue(id + '_timesplayed', timesPlayed)
		DB.setValue(id + '_completed', True)
		self.timesPlayed = timesPlayed
		ACTIVE_SESSION.ensureTimerRunning(False)
		
		self.ui = {}
		
		ACTIVE_SESSION.endGame()
		self.longestJump = ACTIVE_SESSION.getLongestJump()
		
		self.longestJumpRecord = False
		self.gameDurationRecord = False
		self.jumpCountRecord = False
		
		prev = DB.getFloat(id + '_longestjump')
		if self.longestJump > prev:
			DB.setValue(id + '_longestjump', self.longestJump)
			self.longestJumpRecord = True
		
		self.gameDuration =  ACTIVE_SESSION.gameDuration
		if not isWin: # assuming all losses are timeouts since others resolve into restore-replays. 
			self.gameDuration = ACTIVE_SESSION.timeLimitSeconds * 1.0 # avoid slight rounding errors that would make it look unfair. 
		
		if not DB.hasValue(id + '_fastesttime') or DB.getFloat(id + '_fastesttime') > self.gameDuration:
			if self.isWin:
				DB.setValue(id + '_fastesttime', self.gameDuration)
				self.gameDurationRecord = True
		
		self.jumpCount = ACTIVE_SESSION.jumpCount
		if not DB.hasValue(id + '_fewestjumps') or self.jumpCount < DB.getInt(id + '_fewestjumps'):
			if self.isWin:
				DB.setValue(id + '_fewestjumps', self.jumpCount)
				self.jumpCountRecord = True
		
		DB.save()
	
	def update(self, events, dt):
		self.counter += dt
		if self.counter > 3.3:
			for event in events:
				if event.down:
					if event.type in ('space', 'enter'):
						mss = MapSelectScreen()
						# TODO: set the index of the cursor to the next map
						self.next = TransitionScene(self, mss)
	
	def render(self):
		self.bg.render()
		self.overlay.blitSimple(0, 0)
		
		self.getTextLabel('title', "DELIVERY SUCCESSFUL!" if self.isWin else "TIME'S UP", 'XL', 100, 50).render()
		
		cols = [100, 300, 500]
		y = 250
		
		if self.counter > 1:
			self.getTextLabel('attemptLabel', "Attempt #" + str(self.timesPlayed), 'L', cols[0], y).render()
		
		y += 80
		if self.counter > 1.5:
			self.getTextLabel('timeLabel', "Duration:", 'L', cols[0], y).render()
			self.getTextLabel('timeValue', formatTime(self.gameDuration), 'L', cols[1], y).render()
			if self.gameDurationRecord:
				self.bounceText(self.getTextLabel('timeRecord', "NEW RECORD!", 'M', cols[2], y), cols[2], y).render()
		
		y += 80
		if self.counter > 2:
			self.getTextLabel('jumpslabel', "Total Jumps:", 'L', cols[0], y).render()
			self.getTextLabel('jumpsValue', str(self.jumpCount), 'L', cols[1], y).render()
			if self.jumpCountRecord:
				self.bounceText(self.getTextLabel('jumpsRecord', "NEW RECORD!", 'M', cols[2], y), cols[2], y).render()
		
		y += 80
		if self.counter > 2.5:
			self.getTextLabel('jumpDurlabel', "Longest Jump:", 'L', cols[0], y).render()
			self.getTextLabel('jumpDurValue', formatTime(self.longestJump), 'L', cols[1], y).render()
			if self.longestJumpRecord:
				self.bounceText(self.getTextLabel('jumpDurRecord', "NEW RECORD!", 'M', cols[2], y), cols[2], y).render()
		
		y += 80
		
		if self.counter > 3.3:
			self.bounceText(self.getTextLabel('pressenter', "Press ENTER or something", 'S', cols[1], y), cols[1], y, True).render()
		
	def bounceText(self, lbl, x, ybase, isSlow = False):
		if isSlow:
			y = ybase - 5 * math.sin(self.counter * TWO_PI / 2)
		else:
			y = ybase - abs(10 * math.sin(self.counter * TWO_PI * 2))
		lbl.setPosition(x, int(y))
		return lbl
	
	
	def getTextLabel(self, id, text, size, x, y):
		output = self.ui.get(id)
		if output == None:
			output = Q.renderText(text, size, x, y)
			self.ui[id] = output
		return output
		



def main():
	if DB.getBoolean('intro_shown'):
		start = TitleScene()
	else:
		start = CutScene()
	Q.openWindow("Pentomino's Pizza", 800, 600, start)
	
main()
