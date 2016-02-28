class PlayScene:
	def __init__(self):
		self.next = self
		self.bodies = [
			GravityBody(300, 300, 150, 'rocks/rock3.png', 1 / 30.0),
			GravityBody(600, 500, 150, 'rocks/rock3.png', -1 / 50.0),
		]
	
	def update(self, events, dt):
		for body in self.bodies:
			body.update(self)
	
	def render(self):
		Q.fill(0, 10, 40)
		
		for body in self.bodies:
			body.render()