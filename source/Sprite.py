PLAYER_WALK_VELOCITY = 2.7
PLAYER_JUMP_VELOCITY = 470.0
ASTEROID_GRAVITY_COEFFICIENT = 5000.0 # make bigger for stronger gravity

# If enabled, will skip every other update phase and apply that dt to the next update phase's dt value to ensure that I'm incorporating dt correctly into my calculations
# Be sure to set this to true every once in a while to test.
DT_TEST_ENABLED = False

class Sprite:

	def __init__(self, type, startType, x_or_body, y_or_theta):
		self.r = 10
		self.images = {}
		self.type = type
		if type == 'player':
			self.images['left'] = [GfxImage('sprites/delete-left-0.png'), GfxImage('sprites/delete-left-1.png')]
			self.images['right'] = [GfxImage('sprites/delete-right-0.png'), GfxImage('sprites/delete-right-1.png')]
		elif type == 'ship':
			self.images['left'] = [GfxImage('sprites/ship/ship.png')]
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
		
		# for DT_TEST_ENABLED
		self.counter = 0
		self.dt_backlog = 0.0
		
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
			
	
	def applyWalk(self, dir):
		if dir != 0:
			self.facingLeft = dir < 0
			v = PLAYER_WALK_VELOCITY
			if self.ground != None:
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
					theta = math.atan2(-dy, -dx)
					self.thetaFromGround = theta - body.theta
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
			twoPi = 2 * 3.14159265358979
			targetTheta = math.atan2(-dy, -dx) % twoPi
			currentTheta = self.theta % twoPi
			dTheta = currentTheta - targetTheta
			if dTheta > 3.14159265358979:
				currentTheta -= twoPi
			if dTheta < -3.14159265358979:
				targetTheta -= twoPi
			
			r = .9 ** (dt / (1.0 / 30))
			ar = 1.0 - r
			self.theta = r * currentTheta + ar * targetTheta
		
		self.vx += gx * dt
		self.vy += gy * dt
	
	def updateForGround(self, scene, dt):
		v = self.angularVelocity
		r = self.ground.radius
		# Law-O-Cosines
		theta = math.acos(((v ** 2) - 2 * (r ** 2)) / (-2 * (r ** 2)))
		if v < 0:
			self.thetaFromGround -= theta
		else:
			self.thetaFromGround += theta
		
		self.angularVelocity *= .8 ** (dt / (1.0 / 30))
	
	def update(self, scene, dt):
		if self.ground == None:
			self.updateForFloating(scene, dt)
		else:
			self.updateForGround(scene, dt)
		self.hitBox = None
		
	def render(self, rc, cx, cy):
		hb = self.getHitBox()
		imgs = self.images['left'] if self.facingLeft else self.images['right']
		img = imgs[(rc / 4) % len(imgs)]
		if self.ground == None:
			img.blitRotation(hb[0] + cx, hb[1] + cy, self.theta)
		else:
			img.blitRotation(hb[0] + cx, hb[1] + cy, self.ground.theta + self.thetaFromGround)
			
		