class OptionsMenu:
	def __init__(self):
		self.next = self
		self.index = 0
		self.images = {}
		
	
	def update(self, events, dt):
		enter = False
		for event in events:
			if event.down:
				if event.type == 'up':
					self.index -= 1
				elif event.type == 'down':
					self.index += 1
				elif event.type in ('space', 'enter'):
					enter = True
		if self.index < 0: self.index = 0
		elif self.index > 1: self.index = 1
		
		if enter:
			if self.index == 0:
				DB.setValue('magic', not DB.getBoolean('magic'))
				DB.save()
			else:
				self.next = TransitionScene(self, TitleScene())
	
	def render(self):
		self.getImage('background/space1.png').blitSimple(0, 0)
		options = ['Magic', 'Back to Title Screen']
		if not DB.getBoolean('magic'):
			options[0] = 'More Magic'
		y = 300
		for i in range(2):
			x = 200
			self.getText(options[i], x, y).render()
			if i == self.index:
				yOffset = abs(math.sin(time.time() * 2 * 3.14159)) * 15
				x -= 70
				self.getImage('menus/pizza.png').blitSimple(x, y - 25 - yOffset)
			y += 100
	
	def getText(self, text, x, y):
		key = 'K:' + text
		img = self.images.get(key)
		if img == None:
			img = Q.renderText(text, 'L', x, y)
			self.images[key] = img
		return img
		
	
	def getImage(self, path):
		img = self.images.get(path)
		if img == None:
			img = GfxImage(path)
			self.images[path] = img
		return img