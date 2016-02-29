
class GravityBody:
	def __init__(self, x, y, radius, imagePath, rps, typeFlag = None):
		self.x = x + 0.0
		self.y = y + 0.0
		self.radius = radius
		self.image = GfxImage(imagePath)
		self.theta = random.random() * 2 * 3.14159
		self.rps = rps
		self.gravity = radius / 100.0
		self.isWater = False
		self.isVolcano = False
		imgWH = (radius * 2, radius * 2)
		if typeFlag == 'water':
			self.isWater = True
		elif typeFlag == 'volcano':
			self.isVolcano = True
			imgWH = (radius * 2.6, radius * 2.6)
		
		self.image.setSize(imgWH[0], imgWH[1])
	
	def update(self, scene, dt):
		self.theta += 2 * 3.14159265358979 * self.rps * dt
	
	def render(self, cx, cy):
		self.image.blitRotation(self.x + cx, self.y + cy, self.theta)
