
class GravityBody:
	def __init__(self, x, y, radius, imagePath, rps):
		self.x = x + 0.0
		self.y = y + 0.0
		self.radius = radius
		self.image = imagePath
		self.theta = random.random() * 2 * 3.14159
		self.rps = rps
	
	def update(self, scene):
		self.theta += 2 * 3.14159 * self.rps / 30
	
	# TODO: scene offset
	def render(self, screen, rc):
		img = IMAGES.getRotated(self.image, self.theta)
		x = int(self.x - img.get_width() / 2)
		y = int(self.y - img.get_height() / 2)
		screen.blit(img, (x, y))
