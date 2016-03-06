LAVA_EXIT_VELOCITY = 150 # pixels / sec

class LavaBall:
	def __init__(self, volcano):
		self.body = volcano
		self.x = self.body.x
		self.y = self.body.y
		self.path = None
		self.lifetime = 0
		self.images = [GfxImage('rocks/lavasplash1.png'), GfxImage('rocks/lavasplash2.png')]
		self.image = self.images[0]
	
	def update(self, scene, dt):
		
		if self.path == None:
			theta = int(random.random() * 3) * TWO_PI / 3 + PI / 2 + 8 - .07
			theta += self.body.theta
			self.lifetime = 0
			self.path = theta
			self.image = random.choice(self.images)
		
		self.lifetime += dt
		
		r = self.body.radius + self.lifetime * LAVA_EXIT_VELOCITY
		
		self.x = math.cos(self.path) * r + self.body.x
		self.y = math.sin(self.path) * r + self.body.y
		
		if r - self.body.radius > 300:
			self.path = None
	
	def render(self, cx, cy):
		self.image.blitRotation(self.x + cx, self.y + cy, self.lifetime * 2)