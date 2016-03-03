class ActiveSession:
	def __init__(self):
		self.startTime = 0
	
	def startGame(self):
		self.startTime = time.time()
		self.longestJump = 0.0
		self.currentJump = 0.0
		self.jumpCount = 0
		self.isJumpRecord = False
	
	def startJump(self):
		self.jumpCount += 1
		self.currentJump = time.time()
	
	def endJump(self):
		jumpDuration = time.time() - self.currentJump
		if jumpDuration > self.longestJump:
			self.longestJump = jumpDuration
			self.isJumpRecord = True
		self.currentJump = None
	
	def popJumpRecordStatus(self):
		if self.isJumpRecord:
			self.isJumpRecord = False
			return True
		return False
	
	def getLongestJump(self):
		return self.longestJump
	

ACTIVE_SESSION = ActiveSession()
