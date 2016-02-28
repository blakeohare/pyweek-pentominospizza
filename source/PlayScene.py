class PlayScene:
	def __init__(self):
		self.next = self
	
	def update(self, events, pressedKeys):
		pass
	
	def render(self, screen, rc):
		screen.fill((255, 0, 0))