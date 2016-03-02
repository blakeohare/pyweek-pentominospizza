class CutScene:
	def __init__(self):
		self.next = self
		self.stub = None
	
	def update(self, events, dt):
		for event in events:
			if event.down and (event.type == 'enter' or event.type == 'space'):
				self.next = TransitionScene(self, TitleScene())
				DB.setValue('intro_shown', True)
				DB.save()
				
	
	def render(self):
		if self.stub == None:
			self.stub = GfxImage('cutscene/page1.png')
		self.stub.blitSimple(0, 0)