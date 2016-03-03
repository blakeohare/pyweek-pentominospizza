_BODY_TYPE_INFO = {
	# image name, radius
	'halfgrass': ('halfgrass', 150),
	'lava': ('lava', 150),
	'rock1': ('rock1', 150),
	'rock2': ('rock2', 150),
	'rock3': ('rock3', 150),
	'rock4': ('rock4', 150),
	'volcano': ('volcano', 150),
	'water': ('water', 150),
}

class PlayScene:
	# Restore type is either 'M' for map or 'S' for state
	# arg is level string ID for M and another playscene for S
	def __init__(self, restoreType, arg):
		self.next = self
		self.bg = GfxImage('background/space4.png')
		self.pointer = GfxImage('pointer.png')
		
		self.sprites = []
		self.player = None
		self.bodies = []
		
		self.hoverTime = None # counter for when you are jumping
		self.recordIndicator = None
		self.countdownLabel = None
		
		if restoreType == 'M':
			self.level = Level(arg)
			self.id = arg
			for body in self.level.stuff:
				type, x, y, sprites = body
				imgPath, radius = _BODY_TYPE_INFO[type]
				flag = None
				if type == 'water':
					flag = 'water'
				elif type == 'volcano':
					flag = 'volcano'
				elif type == 'lava':
					flag = 'lava'
				body = GravityBody(x, y, radius, 'rocks/' + imgPath + '.png', 1 / 30.0, flag)
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
				gb = GravityBody(0, 0, 150, 'rocks/rock1.png', 0, None) # dummy value
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
			if event.type == 'space' and event.down:
				jump = True
			elif event.type == 'enter' and event.down:
				self.next = PauseScreen(self)
		
		self.player.applyJump(jump, dt)
		
		for deb in self.debris:
			deb.update(self, dt)
		for body in self.bodies:
			body.update(self, dt)
		for sprite in self.sprites:
			sprite.update(self, dt)
	
	def triggerWin(self):
		self.next = WinScreen(self)
	
	def triggerDeath(self):
		self.next = TransitionScene(self, ['S', self])
	
	def render(self):
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
		
		t = int(time.time() * FPS)
		
		cx = Q.width / 2 - self.cameraCurrentX
		cy = Q.height / 2 - self.cameraCurrentY
		
		for deb in self.debris:
			deb.render(cx, cy)
		
		for body in self.bodies:
			body.render(cx, cy)
		
		for sprite in self.sprites:
			sprite.render(t, cx, cy)
			
		
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
				#print pt, ang, segment
				if pt != None:
					#print pt
					self.pointer.blitRotation(pt[0] + 400, pt[1] + 300, ang)
					break
			
			
			
			