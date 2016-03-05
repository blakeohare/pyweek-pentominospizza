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
			
		
		