class PauseScreen:

	def __init__(self, bg):
		self.counter = 0
		self.next = self
		self.bg = bg
		self.overlay = GfxImage('dark_overlay.png')
		self.overlay.setSize(800, 600)
		self.index = 0
		
		x = 200
		y = 250
		margin = 100
		self.options = [
			Q.renderText('Resume', 'L', x, y),
			Q.renderText('Restart', 'L', x, y + margin),
			Q.renderText('Back to Menu', 'L', x, y + margin * 2),
		]
		
		self.cursor = GfxImage('menus/pizza.png')
	
	def update(self, events, dt):
		self.counter += dt
		ACTIVE_SESSION.ensureTimerRunning(False)
		confirm = False
		for event in events:
			if event.down:
				if event.type == 'space' or event.type == 'enter':
					confirm = True
				elif event.type == 'up':
					self.index -= 1
				elif event.type == 'down':
					self.index += 1
		if self.index < 0:
			self.index = 0
		if self.index > 2:
			self.index = 2
		
		if confirm:
			if self.index == 0:
				self.next = self.bg
				self.next.next = self.next
			elif self.index == 1:
				self.next = TransitionScene(self, ['M', self.bg.id])
			elif self.index == 2:
				self.next = TransitionScene(self, MapSelectScreen())
					
		
	
	def render(self):
		self.bg.render()
		self.overlay.blitSimple(0, 0)
		
		for option in self.options:
			option.render()
		
		x = 50
		y = 250 + 100 * self.index - abs(15 * math.sin(self.counter * TWO_PI))
		
		self.cursor.blitSimple(x, y)
		
		