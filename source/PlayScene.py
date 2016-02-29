_BODY_TYPE_INFO = {
	# image name, radius
	'halfgrass': ('halfgrass', 150),
	'rock1': ('rock1', 150),
	'rock2': ('rock2', 150),
	'rock3': ('rock3', 150),
	'rock4': ('rock4', 150),
}



class PlayScene:
	def __init__(self):
		self.next = self
		self.bg = GfxImage('background/space4.png')
		
		self.level = Level('level1')
		
		self.sprites = []
		self.player = None
		self.bodies = []
		
		for body in self.level.stuff:
			type, x, y, sprites = body
			imgPath, radius = _BODY_TYPE_INFO[type]
			body = GravityBody(x, y, radius, 'rocks/' + imgPath + '.png', 1 / 30.0)
			for sprite in sprites:
				spriteInstance = None
				type, angle = sprite
				if type == 'player':
					self.player = Sprite('player', 'G', body, angle)
				elif type == 'store':
					spriteInstance = Sprite('store', 'G', body, angle)
				else:
					print("Unknown sprite type: " + type)
				if spriteInstance != None:
					self.sprites.append(spriteInstance)
			self.bodies.append(body)
		
		if self.player != None:
			# ensure player is rendered last so always on top
			self.sprites.append(self.player)
		self.debris = []
		
		for i in range(10):
			self.debris.append(Debris(1000 * random.random(), random.random() * 1000, 'small-debris' + str(int(random.random() * 8) + 1)))
		
		self.cameraTargetX = None
		self.cameraTargetY = None
		self.cameraCurrentX = None
		self.cameraCurrentY = None
		
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
		
		self.player.applyJump(jump)
		
		for deb in self.debris:
			deb.update(self, dt)
		for body in self.bodies:
			body.update(self, dt)
		for sprite in self.sprites:
			sprite.update(self, dt)
	
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
		
		t = int(time.time() * 30)
		
		cx = Q.width / 2 - self.cameraCurrentX
		cy = Q.height / 2 - self.cameraCurrentY
		
		for deb in self.debris:
			deb.render(cx, cy)
		
		for body in self.bodies:
			body.render(cx, cy)
		
		for sprite in self.sprites:
			sprite.render(t, cx, cy)