
class TitleScene:
	def __init__(self):
		self.next = self
		self.quit_attempt = False
		self.index = 0
		self.counter = 0
		
		self.options = [
			("Play", self.click_play),
			('Options', self.click_options),
			('Credits', self.click_credits),
			('Exit', self.click_exit),
		]
	
	def update(self, events, dt):
		self.counter = int(time.time() * 30)
		enter = False
		for event in events:
			if event.down:
				if event.type == 'up':
					self.index -= 1
					self.counter = 0
				elif event.type == 'down':
					self.index += 1
					self.counter = 0
				elif event.type == 'enter' or event.type == 'space':
					enter = True
		
		if self.index < 0: self.index = 0
		if self.index >= len(self.options): self.index = len(self.options) - 1
		
		if enter:
			self.options[self.index][1]()
		
	def click_play(self):
		self.next = TransitionScene(self, PlayScene())
	
	def click_options(self):
		pass
	
	def click_credits(self):
		pass
	
	def click_exit(self):
		Q.quit()
		
	def render(self):
		Q.drawImageTopLeft('background/space1.png', 0, 0)
		
		x = 200
		y = 200
		i = 0
		for option in self.options:
			text = option[0]
			yOffset = 0
			if i == self.index:
				yOffset = int(abs(math.sin(self.counter * 2 * 3.14159 / 30) * 8))
			Q.renderText(text, 'L', x, y - yOffset)
			y += 100
			i += 1
		
		
	