class PlayScene:
	def __init__(self):
		self.next = self
		self.bodies = [
			GravityBody(300, 300, 150, 'rocks/rock3.png', 1 / 20.0),
			GravityBody(600, 500, 150, 'rocks/rock3.png', 1 / 30.0),
		]
		self.sprites = []
		self.player = Sprite('player', 'G', self.bodies[0], 3.14159 / 2)
		self.sprites.append(self.player)
	
	def update(self, events, dt):
		
		dx = 0
		if Q.pressedActions['left']:
			dx = -1
		elif Q.pressedActions['right']:
			dx = 1
		
		self.player.applyWalk(dx)
		
		for body in self.bodies:
			body.update(self, dt)
		for sprite in self.sprites:
			sprite.update(self, dt)
	
	def render(self):
		Q.fill(0, 10, 40)
		
		t = int(time.time() * 30)
		
		for body in self.bodies:
			body.render()
		
		for sprite in self.sprites:
			sprite.render(t)