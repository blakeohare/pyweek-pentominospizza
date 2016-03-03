class MapSelectScreen:
	def __init__(self):
		self.next = self
		
		self.index = 1
		self.counter = 0
		self.bg = None
		self.cursor = None
		
		self.options = []
		
		self.options.append([
			'BACK',
			20,
			[None],
			['Back to title screen'],
			])
		
		
		for key in MAP_DB.getKeys():
			m = MAP_DB.get(key)
			unlocked = MAP_DB.isUnlocked(m.key)
			fastestTime = None
			longestJump = None
			fewestJumps = None
			timesPlayed = None
			
			title = '(Not unlocked yet)'
			
			if unlocked:
				title = m.name
				if DB.hasValue(key + '_fastesttime'):
					fastestTime = DB.getFloat(key + '_fastesttime')
				if DB.hasValue(key + '_longestjump'):
					longestJump = DB.getFloat(key + '_longestjump')
				if DB.hasValue(key + '_fewesetjumps'):
					fewestJumps = DB.getInt(key + '_fewesetjumps')
				timesPlayed = DB.getInt(key + '_timesplayed')
			
			option = [
				title,
				nstr(timesPlayed),
				formatTime(fastestTime),
				nstr(fewestJumps),
				formatTime(longestJump),
			]
			
			option = [key, 0, [None] * len(option), option] # [0] -> map key, [1] -> bottom padding, [2] -> pyglet label objects, [3] -> raw string values or None if not present
			
			self.options.append(option)
		
	
	def update(self, events, dt):
		self.counter += dt * 30
		confirm = False
		for event in events:
			if event.down:
				if event.type == 'up':
					self.index -= 1
				elif event.type == 'down':
					self.index += 1
				elif event.type == 'space' or event.type == 'enter':
					confirm = True
		
		if self.index < 0:
			self.index = 0
		if self.index >= len(self.options):
			self.index = len(self.options) - 1
		
		if confirm:
			key = self.options[self.index][0]
			if key == 'BACK':
				self.next = TransitionScene(self, TitleScene())
			else:
				ACTIVE_SESSION.startGame()
				self.next = TransitionScene(self, PlayScene('M', key))
		
		
	def render(self):
		if self.bg == None:
			self.bg = GfxImage('background/space1.png')
		self.bg.blitSimple(0, 0)
		
		
		y = 40
		index = -1
		for option in self.options:
			index += 1
			x = 100
			
			if index == self.index:
				# needs to be adjusted to dt
				yOffset = int(abs(math.sin(self.counter * TWO_PI / FPS) * 16))
				if self.cursor == None:
					self.cursor = GfxImage('menus/pizza.png')
				cx = x - 50
				cy = y - yOffset - 30
				self.cursor.blitSimple(cx, cy)
				
			yPad = option[1]
			buttons = option[2]
			text = option[3]
			
			for i in range(len(buttons)):
				button = buttons[i]
				if button == None and text[i] != None:
					button = Q.renderText(text[i], 'M', x, y)
					x += [200, 100, 100, 100, 100, 100][i]
					buttons[i] = button
				
				if button != None:
					button.render()
			
			y += 50 + yPad
		
			