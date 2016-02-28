class Sprite:

	def __init__(self, x, y):
		self.x = x + 0.0
		self.y = y + 0.0
		self.vx = vx
		self.vy = vy
		self.ground = None
		self.thetaFromGround = 0
		self.floatingTheta = 0.0
		
	
	def update(self, scene):
		self.x += self.vx
		self.y += self.vy
	
	def render(self, rc):
		if self.ground == None:
			pass
		else:
			pass
		