class CutScene:
	def __init__(self):
		self.next = self
		self.stub = None
		self.index = 0
		self.state_counter = 0.0
		self.progress = 0.0
		
		self.states = [
			('start', 3),
			('ringring', 2),
			('phone1-normal', 3),
			('ufo-enter', 1),
			('ufo-wait', 1),
			('ufo-blast', 2),
			('white-in', 1),
			('white', 2),
			('white-out', 3),
			('end', 2),
		]
		
		self.images = {}
	
	def render(self):
		if self.index >= len(self.states):
			state = self.states[-1]
		else:
			state = self.states[self.index]
		
		progress = self.state_counter / state[1]
		if progress < 0: progress = 0.0
		elif progress > 1: progress = 1.0
		antiprogress = 1.0 - progress
		id = state[0]
		
		if id == 'start':
			self.blitImage('window-background-small', 350, 50)
			self.blitImage('page1', 0, 0)
		elif id == 'ringring':
			self.blitImage('window-background-small', 350, 50)
			self.blitImage('page1', 0, 0)
			self.drawText("*RING RING*", 566, 31)
		elif id == 'phone1-normal':
			self.blitImage('window-background', 85, 58)
			self.blitImage('window', 0, 0)
		elif id == 'ufo-enter':
			self.blitImage('window-background', 85, 58)
			yStart = -300
			yEnd = 100
			y = progress * yEnd + antiprogress * yStart
			self.blitImage('ufo', 200, y)
			self.blitImage('window', 0, 0)
		elif id == 'ufo-wait':
			self.blitImage('window-background', 85, 58)
			self.blitImage('ufo', 200, 100)
			self.blitImage('window', 0, 0)
		elif id == 'ufo-blast':
			self.blitImage('window-background', 85, 58)
			self.blitImage('beam', 270, 180)
			self.blitImage('ufo', 200, 100)
			self.blitImage('window', 0, 0)
		elif id == 'white-in':
			self.blitImage('window-background', 85, 58)
			self.blitImage('beam', 270, 180)
			self.blitImage('ufo', 200, 100)
			self.blitImage('window', 0, 0)
			self.blitImage('white', 0, 0, progress)
		elif id == 'white':
			self.blitImage('white', 0, 0, 1.0)
		elif id == 'white-out':
			self.blitImage('space-background', 85, 58)
			self.blitImage('space-asteroids', 85, 58)
			self.blitImage('window', 0, 0)
			self.blitImage('white', 0, 0, antiprogress)
		elif id == 'end':
			self.blitImage('space-background', 85, 58)
			self.blitImage('space-asteroids', 85, 58)
			self.blitImage('window', 0, 0)
			
		
			
			
		
	def update(self, events, dt):
		self.state_counter += dt
		if self.index >= len(self.states):
			self.leave()
		
		for event in events:
			if event.down and (event.type == 'enter' or event.type == 'space'):
				self.leave()
		
		if self.index >= len(self.states):
			self.index = len(self.states) - 1
		
		state = self.states[self.index]
		
		total = state[1]
		if self.state_counter >= total:
			self.state_counter = 0
			self.index += 1
		
		self.progress = 1.0 * self.state_counter / total

	def leave(self):
		self.next = TransitionScene(self, TitleScene())
		DB.setValue('intro_shown', True)
		DB.save()
	
	def drawText(self, text, x, y):
		txt = self.images.get('T:' + text)
		if txt == None:
			txt = Q.renderText(text, 'L', x, y)
			self.images['T:' + text] = txt
		
		txt.render()
	
	def blitImage(self, path, x, y, opacityRatio = None):
		img = self.images.get(path)
		if img == None:
			img = GfxImage('cutscene/' + path + '.png')
			self.images[path] = img
		
		if (opacityRatio != None):
			alpha = int(opacityRatio * 255)
			if alpha < 0: alpha = 0
			if alpha > 255: alpha = 255
			img.sprite.opacity = alpha
		
		img.blitSimple(x, y)
	