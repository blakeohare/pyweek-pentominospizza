class ActiveSession:
	def __init__(self):
		self.startTime = 0
	
	def startGame(self, id):
		self.startTime = time.time()
		self.longestJump = 0.0
		self.currentJump = None
		self.jumpCount = 0
		self.isJumpRecord = False
		self.lastKnownJumpRecord = DB.getFloat(id + '_longestjump')
	
	def startJump(self):
		self.jumpCount += 1
		self.currentJump = time.time()
		self.isJumpRecord = False
	
	def endJump(self):
		jumpDuration = time.time() - self.currentJump
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
		return time.time() - self.currentJump
	
	def getLongestJump(self):
		return self.longestJump
	
	def endGame(self):
		self.gameDuration = time.time() - self.startTime
		
	

ACTIVE_SESSION = ActiveSession()
