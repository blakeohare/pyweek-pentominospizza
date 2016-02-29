class PlayScene:
	def __init__(self):
		self.next = self
		self.bg = GfxImage('background/space4.png')
		self.bodies = [
			GravityBody(300, 300, 150, 'rocks/rock3.png', 1 / 20.0),
			GravityBody(600, 500, 150, 'rocks/rock3.png', 1 / 30.0),
		]
		
		self.debris = [
			Debris(100, 100, 'small-debris1'),
			Debris(600, 100, 'small-debris2'),
		]
		
		self.player = Sprite('player', 'G', self.bodies[0], 3.14159 / 2)
		self.ship = Sprite('ship', 'G', self.bodies[1], 3.14159 / 2)
		self.sprites = [self.player, self.ship]
		
		self.inputTarget = self.player
		self.cameraTargetX = None
		self.cameraTargetY = None
		self.cameraCurrentX = None
		self.cameraCurrentY = None
		
	
	def update(self, events, dt):
		dx = 0
		if Q.pressedActions['left']:
			dx = -1
			self.inputTarget.facingLeft = True
		elif Q.pressedActions['right']:
			dx = 1
			self.inputTarget.facingLeft = False
			
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
		
		hb = self.inputTarget.getHitBox()
		
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