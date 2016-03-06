class CreditsScene:
	def __init__(self):
		self.next = self
		self.things = {}
		self.counter = 0
	
	def update(self, events, dt):
		self.counter += dt
		
		for event in events:
			if event.down and event.type in ('space', 'enter'):
				self.next = TransitionScene(self, TitleScene())
	
	
	def render(self):
		bg = self.things.get('bg')
		if bg == None:
			bg = GfxImage('background/space1.png')
			self.things['bg'] = bg
		
		bg.blitSimple(0, 0)
		
		self.getText('Programming', 'S', 80, 200).render()
		self.getText("Blake O'Hare", 'L', 80, 260).render()
		
		self.getText('Art', 'S', 370, 200).render()
		self.getText('Sophia Baldonado', 'L', 370, 260).render()
		
		y = 450
		self.getText('Press ENTER or something', 'S', 300, y - abs(int(math.sin(self.counter * TWO_PI) * 15))).render()
		
	
	def getText(self, text, size, x, y):
		t = self.things.get(text)
		if t == None:
			t = Q.renderText(text, size, x, y)
			self.things[text] = t
		else:
			t.setPosition(x, y)
		return t