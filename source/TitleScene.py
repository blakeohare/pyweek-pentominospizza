
class TitleScene:
	def __init__(self):
		self.next = self
		self.quit_attempt = False
		self.index = 0
		self.counter = 0
		
		self.cursor = None
		
		self.options = [
			["Play", self.click_play, None],
			["Replay Intro", self.click_intro, None],
			['Options', self.click_options, None],
			['Credits', self.click_credits, None],
			['Exit', self.click_exit, None],
		]
		self.bg = None
		self.textCounter = None
		DB.setValue('views', DB.getInt('views', 0) + 1)
		DB.save()
	
	def update(self, events, dt):
		self.counter += dt * 30
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
	
	def click_intro(self):
		self.next = TransitionScene(self, CutScene())
	
	def click_play(self):
		self.next = TransitionScene(self, MapSelectScreen())
	
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
				yOffset = int(abs(math.sin(self.counter * TWO_PI / FPS) * 16))
				if self.cursor == None:
					self.cursor = GfxImage('menus/pizza.png')
				self.cursor.blitSimple(x - 100, y - yOffset - 30)
			obj = option[2]
			if obj == None:
				obj = Q.renderText(text, 'L', x, y)
				option[2] = obj
			obj.setPosition(x, y)
			
			obj.render()
			
			
			
			y += 80
			i += 1
		
		if self.textCounter == None:
			views = str(DB.getInteger('views', 0))
			last = views[-1:]
			last2 = views[-2:]
			if last == '1' and last2 != '11': 
				suffix = 'st'
			elif last == '2' and last2 != '12':
				suffix = 'nd'
			elif last == '3' and last2 != '13':
				suffix = 'rd'
			else:
				suffix = 'th'
				
			self.textCounter = Q.renderText("This is the " + views + suffix + " time you've viewed this screen.", 'M', 0, 20)
		
		self.textCounter.render()
	