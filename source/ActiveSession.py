class ActiveSession:
	def __init__(self):
		self.startTime = 0
		self.id = None
	
	def startGame(self, id, timeLimitSeconds):
		self.id = id
		self.timeLimitSeconds = timeLimitSeconds
		self.startTime = time.time()
		self.longestJump = 0.0
		self.currentJump = None
		self.jumpCount = 0
		self.isJumpRecord = False
		self.lastKnownJumpRecord = DB.getFloat(id + '_longestjump')
		self.timerRunning = True
		self.timeAccrued = 0.0
	
	def startJump(self):
		self.jumpCount += 1
		self.currentJump = self.getCurrentTime()
		self.isJumpRecord = False
	
	def ensureTimerRunning(self, toggle):
		if toggle == self.timerRunning:
			return
		
		self.timerRunning = toggle
		if toggle:
			self.startTime = time.time() - self.timeAccrued
		else:
			self.timeAccrued = time.time() - self.startTime
	
	def getCurrentTime(self):
		if self.timerRunning:
			return time.time() - self.startTime
		else:
			return self.timeAccrued
	
	def endJump(self):
		jumpDuration = self.getCurrentTime() - self.currentJump
		if jumpDuration > self.longestJump:
			self.longestJump = jumpDuration
		if jumpDuration > self.lastKnownJumpRecord:
			self.isJumpRecord = True
			self.lastKnownJumpRecord = jumpDuration
		self.currentJump = None
	
	def popJumpRecordStatus(self):
		if self.isJumpRecord:
			self.isJumpRecord = False
			return True
		return False
	
	def getCurrentJump(self):
		if self.currentJump == None:
			return None
		return self.getCurrentTime() - self.currentJump
	
	def getLongestJump(self):
		return self.longestJump
	
	def endGame(self):
		self.gameDuration = time.time() - self.startTime
		
	

ACTIVE_SESSION = ActiveSession()
