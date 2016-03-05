# This is now repurposed for when you lose as well as it needs to apply the record for longest jump

class WinScreen:
	def __init__(self, bg, isWin = True):
		self.next = self
		self.isWin = isWin
		self.bg = bg
		self.overlay = GfxImage('dark_overlay.png')
		self.overlay.setSize(800, 600)
		self.counter = 0
		self.isLongestJumpRecord = False
		id = self.bg.id
		timesPlayed = DB.getInt(id + '_timesplayed') + 1
		DB.setValue(id + '_timesplayed', timesPlayed)
		DB.setValue(id + '_completed', True)
		self.timesPlayed = timesPlayed
		ACTIVE_SESSION.ensureTimerRunning(False)
		
		self.ui = {}
		
		ACTIVE_SESSION.endGame()
		self.longestJump = ACTIVE_SESSION.getLongestJump()
		
		self.longestJumpRecord = False
		self.gameDurationRecord = False
		self.jumpCountRecord = False
		
		prev = DB.getFloat(id + '_longestjump')
		if self.longestJump > prev:
			DB.setValue(id + '_longestjump', self.longestJump)
			self.longestJumpRecord = True
		
		self.gameDuration =  ACTIVE_SESSION.gameDuration
		if not isWin: # assuming all losses are timeouts since others resolve into restore-replays. 
			self.gameDuration = ACTIVE_SESSION.timeLimitSeconds * 1.0 # avoid slight rounding errors that would make it look unfair. 
		
		if not DB.hasValue(id + '_fastesttime') or DB.getFloat(id + '_fastesttime') > self.gameDuration:
			if self.isWin:
				DB.setValue(id + '_fastesttime', self.gameDuration)
				self.gameDurationRecord = True
		
		self.jumpCount = ACTIVE_SESSION.jumpCount
		if not DB.hasValue(id + '_fewestjumps') or self.jumpCount < DB.getInt(id + '_fewestjumps'):
			if self.isWin:
				DB.setValue(id + '_fewestjumps', self.jumpCount)
				self.jumpCountRecord = True
		
		DB.save()
	
	def update(self, events, dt):
		self.counter += dt
		if self.counter > 3.3:
			for event in events:
				if event.down:
					if event.type in ('space', 'enter'):
						mss = MapSelectScreen()
						# TODO: set the index of the cursor to the next map
						self.next = TransitionScene(self, mss)
	
	def render(self):
		self.bg.render()
		self.overlay.blitSimple(0, 0)
		
		self.getTextLabel('title', "DELIVERY SUCCESSFUL!" if self.isWin else "TIME'S UP", 'XL', 100, 50).render()
		
		cols = [100, 300, 500]
		y = 250
		
		if self.counter > 1:
			self.getTextLabel('attemptLabel', "Attempt #" + str(self.timesPlayed), 'L', cols[0], y).render()
		
		y += 80
		if self.counter > 1.5:
			self.getTextLabel('timeLabel', "Duration:", 'L', cols[0], y).render()
			self.getTextLabel('timeValue', formatTime(self.gameDuration), 'L', cols[1], y).render()
			if self.gameDurationRecord:
				self.bounceText(self.getTextLabel('timeRecord', "NEW RECORD!", 'M', cols[2], y), cols[2], y).render()
		
		y += 80
		if self.counter > 2:
			self.getTextLabel('jumpslabel', "Total Jumps:", 'L', cols[0], y).render()
			self.getTextLabel('jumpsValue', str(self.jumpCount), 'L', cols[1], y).render()
			if self.jumpCountRecord:
				self.bounceText(self.getTextLabel('jumpsRecord', "NEW RECORD!", 'M', cols[2], y), cols[2], y).render()
		
		y += 80
		if self.counter > 2.5:
			self.getTextLabel('jumpDurlabel', "Longest Jump:", 'L', cols[0], y).render()
			self.getTextLabel('jumpDurValue', formatTime(self.longestJump), 'L', cols[1], y).render()
			if self.longestJumpRecord:
				self.bounceText(self.getTextLabel('jumpDurRecord', "NEW RECORD!", 'M', cols[2], y), cols[2], y).render()
		
		y += 80
		
		if self.counter > 3.3:
			self.bounceText(self.getTextLabel('pressenter', "Press ENTER or something", 'S', cols[1], y), cols[1], y, True).render()
		
	def bounceText(self, lbl, x, ybase, isSlow = False):
		if isSlow:
			y = ybase - 5 * math.sin(self.counter * TWO_PI / 2)
		else:
			y = ybase - abs(10 * math.sin(self.counter * TWO_PI * 2))
		lbl.setPosition(x, int(y))
		return lbl
	
	
	def getTextLabel(self, id, text, size, x, y):
		output = self.ui.get(id)
		if output == None:
			output = Q.renderText(text, size, x, y)
			self.ui[id] = output
		return output
		