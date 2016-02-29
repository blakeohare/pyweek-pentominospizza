_DEBRIS_OFFSETS = (
	(0, 0),
	(1, 0),
	(0, 1),
	(1, 1),
)

class Debris:
	def __init__(self, x, y, type):
		self.x = x
		self.y = y
		self.type = type
		self.theta = random.random() * 2 * 3.14159265358979
		self.img = GfxImage('rocks/' + type + '.png')
		self.angularVelocity = random.random() / 25.0
	
	def update(self, scene, dt):
		self.theta += self.angularVelocity * (dt / (1.0 / 30))
	
	def render(self, cx, cy):
		x = (self.x + cx * .6) % 1000 - 500
		y = (self.y + cy * .6) % 1000 - 500
		
		for offset in _DEBRIS_OFFSETS:
			ox, oy = offset
			self.img.blitRotation(x + ox * 1000, y + oy * 1000, self.theta)
