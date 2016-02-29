
class TitleScene:
	def __init__(self):
		self.next = self
		self.quit_attempt = False
		self.index = 0
		self.counter = 0
		
		self.options = [
			["Play", self.click_play, None],
			['Options', self.click_options, None],
			['Credits', self.click_credits, None],
			['Exit', self.click_exit, None],
		]
		self.bg = None
	
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
		if self.bg == None:
			self.bg = GfxImage('background/space1.png')
			
		self.bg.blitSimple(0, 0)
		
		x = 200
		y = 200
		i = 0
		for option in self.options:
			text = option[0]
			yOffset = 0
			if i == self.index:
				# needs to be adjusted to dt
				yOffset = int(abs(math.sin(self.counter * TWO_PI / FPS) * 8))
			yValue = y - yOffset
			obj = option[2]
			if obj == None:
				obj = Q.renderText(text, 'L', x, yValue)
				option[2] = obj
			obj.setPosition(x, yValue)
			
			obj.render()
			
			y += 100
			i += 1
		
		
	