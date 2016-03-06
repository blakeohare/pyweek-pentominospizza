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
		