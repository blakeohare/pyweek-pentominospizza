class PauseScreen:

	def __init__(self, bg):
		self.next = self
		self.bg = bg
		self.overlay = GfxImage('dark_overlay.png')
		self.overlay.setSize(800, 600)
		self.index = 0
	
	def update(self, events, dt):
		ACTIVE_SESSION.ensureTimerRunning(False)
		for event in events:
			if event.down:
				if event.type == 'space' or event.type == 'enter':
					self.next = self.bg
					self.next.next = self.next
	
	def render(self):
		self.bg.render()
		self.overlay.blitSimple(0, 0)
		