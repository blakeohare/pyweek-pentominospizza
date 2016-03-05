
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
		self.chet = None
		self.title = None
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
		self.next = OptionsMenu()
	
	def click_credits(self):
		pass
	
	def click_exit(self):
		# Not sure if this is considered "clean" in Pyglet, but the recommended way didn't seem to work. But it's PyWeek so this is good enough for me.
		os.sys.exit()
	
	def render(self):
		if self.bg == None:
			self.bg = GfxImage('background/space1.png')
			
		self.bg.blitSimple(0, 0)
		
		if self.chet == None:
			self.chet = GfxImage('sprites/chet-walk-1.png')
			r = 1.0 * self.chet.width / self.chet.height
			self.chet.setSize(400 * r, 400)
		self.chet.blitSimple(100, 200)
		
		if self.title == None:
			self.title = GfxImage('menus/title.png')
		self.title.blitSimple(50, 10)
		
		x = 480
		y = 100
		i = 0
		for option in self.options:
			text = option[0]
			yOffset = 0
			if i == self.index:
				# needs to be adjusted to dt
				yOffset = int(abs(math.sin(self.counter * TWO_PI / FPS) * 16))
				if self.cursor == None:
					self.cursor = GfxImage('menus/pizza.png')
				self.cursor.blitSimple(x - 70, y - yOffset - 20)
			obj = option[2]
			if obj == None:
				obj = Q.renderText(text, 'XL', x, y)
				option[2] = obj
			obj.setPosition(x, y)
			
			obj.render()
			
			
			
			y += 100
			i += 1
		
	