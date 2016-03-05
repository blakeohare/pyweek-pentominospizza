PLAYER_WALK_VELOCITY = 6.0
PLAYER_JUMP_VELOCITY = 470.0
ASTEROID_GRAVITY_COEFFICIENT = 5000.0 # make bigger for stronger gravity

# If enabled, will skip every other update phase and apply that dt to the next update phase's dt value to ensure that I'm incorporating dt correctly into my calculations
# Be sure to set this to true every once in a while to test.
DT_TEST_ENABLED = False

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
		imgs = self.images['left'] if self.facingLeft else self.images['right']
		img = imgs[(int(rc) // 4) % len(imgs)]
		x = hb[0] + cx
		y = hb[1] + cy
		if self.ground == None:
			img.blitRotation(x, y, self.theta)
		else:
			img.blitRotation(x, y, self.ground.theta + self.thetaFromGround)
		
		if self.isPlayer:
			currentJump = ACTIVE_SESSION.getCurrentJump()
			if currentJump != None and currentJump > 1:
				lbl = Q.renderText(formatTime(currentJump), 'M', x - 8, y - 40)
				lbl.render()
				
				
			
		