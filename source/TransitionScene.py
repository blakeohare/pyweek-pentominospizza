TRANSITION_TEMP_IMG = [None]

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
		
	
	def update(self, events, pressed_keys):
		self.counter += 1
		if self.counter < self.half:
			self.bg = self.fromScene
			progress = 1.0 * self.counter / self.half
		else:
			self.bg = self.toScene
			progress = 1 - 1.0 * (self.counter - self.half) / self.half
		
		alpha = int(255 * progress)
		if alpha < 0: alpha = 0
		if alpha > 255: alpha = 255
		
		# overlay alpha, that is
		self.alpha = alpha
		
		if self.counter >= self.duration:
			self.next = self.toScene
	
	def render(self, screen, rc):
		self.bg.render(screen, rc)
		overlay = TRANSITION_TEMP_IMG[0]
		if overlay == None:
			overlay = screen.convert()
			overlay.fill((0, 0, 0))
			TRANSITION_TEMP_IMG[0] = overlay
		
		overlay.set_alpha(self.alpha)
		
		screen.blit(overlay, (0, 0))

