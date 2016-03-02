class WinScreen:
	def __init__(self, bg):
		self.next = self
		self.bg = bg
		self.overlay = GfxImage('dark_overlay.png')
		self.overlay.setSize(800, 600)
		self.counter = 0
		id = self.bg.level.id
		timesPlayed = DB.getInt(id + '_timesplayed') + 1
		DB.setValue(id + '_timesplayed', timesPlayed)
		DB.setValue(id + '_completed', True)
		DB.save()
		#TODO: add the other fields.
	
	def update(self, events, dt):
		self.counter += dt
		if self.counter > 1:
			for event in events:
				if event.down:
					if event.type in ('space', 'enter'):
						mss = MapSelectScreen()
						# TODO: set the index of the cursor to the next map
						self.next = TransitionScene(self, mss)
	
	def render(self):
		self.bg.render()
		self.overlay.blitSimple(0, 0)