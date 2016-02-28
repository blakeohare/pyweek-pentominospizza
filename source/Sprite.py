class Sprite:

	def __init__(self, type, startType, x_or_body, y_or_theta):
		self.r = 10
		# TODO: apply other types to radius
		
		self.vx = 0
		self.vy = 0
		self.ground = None
		self.thetaFromGround = 0
		self.floatingTheta = 0.0
		self.hitBox = None
		
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
	
	def update(self, scene):
		if self.ground == None:
			self.x += self.vx
			self.y += self.vy
			self.hitBox = None
		else:
			pass # position is landing offset from ground's theta
		
	def render(self, rc):
		if self.ground == None:
			pass
		else:
			pass
		