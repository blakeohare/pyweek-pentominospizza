class WinScreen:
	def __init__(self, bg):
		self.next = self
		self.bg = bg
		self.overlay = GfxImage('dark_overlay.png')
		self.overlay.setSize(800, 600)
		self.counter = 0
		self.isLongestJumpRecord = False
		id = self.bg.id
		timesPlayed = DB.getInt(id + '_timesplayed') + 1
		DB.setValue(id + '_timesplayed', timesPlayed)
		DB.setValue(id + '_completed', True)
		
		ACTIVE_SESSION.endGame()
		longestJump = ACTIVE_SESSION.getLongestJump()
		
		self.longestJumpRecord = False
		self.gameDurationRecord = False
		self.jumpCountRecord = False
		
		prev = DB.getFloat(id + '_longestjump')
		if longestJump > prev:
			self.isLongestJumpRecord = True
			DB.setValue(id + '_longestjump', longestJump)
			self.longestJumpRecord = True
		
		self.gameDuration =  ACTIVE_SESSION.gameDuration
		if not DB.hasValue(id + '_fastesttime') or DB.getFloat(id + '_fastesttime') > self.gameDuration:
			DB.setValue(id + '_fastesttime', self.gameDuration)
			self.gameDurationRecord = True
		
		self.jumpCount = ACTIVE_SESSION.jumpCount
		if not DB.hasValue(id + '_fewestjumps') or self.jumpCount < DB.getInt(id + '_fewestjumps'):
			DB.setValue(id + '_fewestjumps', self.jumpCount)
			self.jumpCountRecord = True
		
		DB.save()
	
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