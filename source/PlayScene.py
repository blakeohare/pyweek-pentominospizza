class PlayScene:
	def __init__(self):
		self.next = self
		self.bodies = [
			GravityBody(300, 300, 150, 'rocks/rock3.png', 1 / 20.0)
		]
	
	def update(self, events, pressedKeys):
		for body in self.bodies:
			body.update(self)
	
	def render(self, screen, rc):
		screen.fill((0, 10, 40))
		
		for body in self.bodies:
			body.render(screen, rc)