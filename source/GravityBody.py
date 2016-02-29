
class GravityBody:
	def __init__(self, x, y, radius, imagePath, rps, typeFlag = None):
		self.x = x + 0.0
		self.y = y + 0.0
		self.radius = radius
		self.image = GfxImage(imagePath)
		self.image.setSize(radius * 2, radius * 2)
		self.theta = random.random() * 2 * 3.14159
		self.rps = rps
		self.gravity = radius / 100.0
		self.isWater = False
		if typeFlag == 'water':
			self.isWater = True
	
	def update(self, scene, dt):
		self.theta += 2 * 3.14159265358979 * self.rps * dt
	
	def render(self, cx, cy):
		self.image.blitRotation(self.x + cx, self.y + cy, self.theta)
