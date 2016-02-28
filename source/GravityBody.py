
class GravityBody:
	def __init__(self, x, y, radius, imagePath, rps):
		self.x = x + 0.0
		self.y = y + 0.0
		self.radius = radius
		self.image = GfxImage(imagePath)
		self.theta = random.random() * 2 * 3.14159
		self.rps = rps
		self.gravity = radius / 100.0
	
	def update(self, scene, dt):
		self.theta += 2 * 3.14159265358979 * self.rps * dt
	
	# TODO: scene offset
	def render(self, cx, cy):
		self.image.blitRotation(self.x + cx, self.y + cy, self.theta)
		#self.image.blitSimple(self.x, self.y)
