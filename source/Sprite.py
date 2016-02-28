class Sprite:

	def __init__(self, type, startType, x_or_body, y_or_theta):
		self.r = 10
		self.images = {}
		self.type = type
		if type == 'player':
			self.images['left'] = [GfxImage('sprites/delete-left-0.png'), GfxImage('sprites/delete-left-1.png')]
			self.images['right'] = [GfxImage('sprites/delete-right-0.png'), GfxImage('sprites/delete-right-1.png')]
		
		self.vx = 0
		self.vy = 0
		self.ground = None
		self.thetaFromGround = 0
		self.floatingTheta = 0.0
		self.hitBox = None
		self.facingLeft = False
		
		if startType == 'G':
			self.ground = x_or_body
			self.thetaFromGround = y_or_theta
		else:
			self.x = x_or_body + 0.0
			self.y = y_or_theta + 0.0
	
	def getHitBox(self):
		if self.hitBox == None:
			if self.ground == None:
				self.hitBox = (self.x, self.y, self.r)
			else:
				r = self.ground.radius + self.r
				x = self.ground.x + r * math.cos(self.thetaFromGround + self.ground.theta)
				y = self.ground.y + r * math.sin(self.thetaFromGround + self.ground.theta)
				self.hitBox = (x, y, self.r)
		return self.hitBox
	
	def applyJump(self, press):
		if press and self.ground != None:
			ground = self.ground
			jumpVelocity = 100.0 # pixels per second
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
			
	
	def applyWalk(self, dx):
		if dx != 0:
			self.facingLeft = dx < 0
			v = .7
			if self.ground != None:
				r = self.ground.radius
				self.thetaFromGround += math.acos(((v ** 2) - 2 * (r ** 2)) / (-2 * (r ** 2))) * dx
			else:
				pass #print("TODO: movement IN SPACE")
	
	def updateForFloating(self, scene, dt):
		self.x += self.vx * dt
		self.y += self.vy * dt
		
		gx = 0.0
		gy = 0.0
		
		for body in scene.bodies:
			dx = body.x - self.x
			dy = body.y - self.y
			dr = self.r + body.radius
			dist = (dx ** 2 + dy ** 2) ** .5
			if dist < 1000:
				if dist <= dr:
					self.ground = body
					theta = math.atan2(dx, dy)
					self.thetaFromGround = theta - body.theta
					return
				
			g = body.gravity / (dist / 200) ** 2 # magic number ahoy
			ux = dx / dist
			uy = dy / dist
			
			gx += g * ux
			gy += g * uy
		
		self.vx += gx
		self.vy += gy
	
	def update(self, scene, dt):
		if self.ground == None:
			self.updateForFloating(scene, dt)
		else:
			# position is landing offset from ground's theta
			pass
		self.hitBox = None
		
	def render(self, rc):
		hb = self.getHitBox()
		if self.ground == None:
			img = self.images['left'][0]
			img.blitRotation(hb[0], hb[1], self.theta)
		else:
			if self.type == 'player':
				imgs = self.images['left'] if self.facingLeft else self.images['right']
				img = imgs[(rc / 4) % len(imgs)]
			else:
				pass
			
			img.blitRotation(hb[0], hb[1], self.ground.theta + self.thetaFromGround)
			
		