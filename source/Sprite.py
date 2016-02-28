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
	
	def applyWalk(self, dx):
		if dx != 0:
			self.facingLeft = dx < 0
			v = .7
			if self.ground != None:
				r = self.ground.radius
				self.thetaFromGround += math.acos(((v ** 2) - 2 * (r ** 2)) / (-2 * (r ** 2))) * dx
			else:
				print("TODO: movement IN SPACE")
	
	def update(self, scene, dt):
		if self.ground == None:
			self.x += self.vx * dt
			self.y += self.vy * dt
		else:
			# position is landing offset from ground's theta
			pass
		self.hitBox = None
		
	def render(self, rc):
		if self.ground == None:
			pass
		else:
			hb = self.getHitBox()
			if self.type == 'player':
				imgs = self.images['left'] if self.facingLeft else self.images['right']
				img = imgs[(rc / 4) % len(imgs)]
			else:
				pass
			
			img.blitRotation(hb[0], hb[1], self.ground.theta + self.thetaFromGround)
			
		