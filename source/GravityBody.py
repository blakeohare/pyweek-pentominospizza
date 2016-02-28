
class GravityBody:
	def __init__(self, x, y, radius, imagePath, rps):
		self.x = x + 0.0
		self.y = y + 0.0
		self.radius = radius
		self.image = GfxImage(imagePath)
		self.theta = random.random() * 2 * 3.14159
		self.rps = rps
	
	def update(self, scene):
		self.theta += 2 * 3.14159 * self.rps / 30
	
	# TODO: scene offset
	def render(self):
		self.image.blitRotation(self.x, self.y, self.theta)
		#self.image.blitSimple(self.x, self.y)
