
class TransitionScene:
	def __init__(self, fromScene, toScene):
		self.next = self
		self.fromScene = fromScene
		self.toScene = toScene
		self.duration = 30
		self.half = self.duration / 2
		self.counter = 0
		self.bg = fromScene
		self.alpha = 0
		
	
	def update(self, events):
		self.counter += 1
		if self.counter < self.half:
			self.bg = self.fromScene
			progress = 1.0 - 1.0 * self.counter / self.half
		else:
			self.bg = self.toScene
			progress = 1.0 * (self.counter - self.half) / self.half
		
		Q.setScreenAlpha(progress)
		
		if self.counter >= self.duration:
			Q.setScreenAlpha(1)
			self.next = self.toScene
	
	def render(self, rc):
		self.bg.render(rc)
