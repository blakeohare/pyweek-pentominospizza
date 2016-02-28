class PlayScene:
	def __init__(self):
		self.next = self
		self.bodies = [
			GravityBody(300, 300, 150, 'rocks/rock3.png', 1),
			GravityBody(600, 500, 150, 'rocks/rock3.png', .5),
		]
		self.sprites = []
		self.player = Sprite('player', 'G', self.bodies[0], 3.14159 / 2)
		self.sprites.append(self.player)
	
	def update(self, events, dt):
		for body in self.bodies:
			body.update(self)
		for sprite in self.sprites:
			sprite.update(self)
	
	def render(self):
		Q.fill(0, 10, 40)
		
		for body in self.bodies:
			body.render()