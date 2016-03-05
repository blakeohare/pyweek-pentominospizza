
GRAVITY_ID_ALLOC = [0]

def getIdFromBody(body):
	if body == None: return None
	return body.id

def getBodyFromId(id, bodies):
	if id == None: return None
	return bodies.get(id)
	
class GravityBody:
	def __init__(self, type, x, y, radius, imagePath, rps, rotRat, typeFlag = None):
		# IF YOU ADD ANYTHING HERE, ADD IT TO SAVE AND RESTORE STATE
		self.type = type
		self.id = GRAVITY_ID_ALLOC[0]
		GRAVITY_ID_ALLOC[0] += 1
		self.x = x + 0.0
		self.y = y + 0.0
		self.radius = radius
		self.rotRat = rotRat
		self.image = GfxImage(imagePath)
		self.theta = random.random() * TWO_PI
		self.rps = rps
		self.gravity = radius / 100.0
		self.isWater = False
		self.isVolcano = False
		self.isDeathy = False
		imgWH = (radius * 2, radius * 2)
		if typeFlag == 'water':
			self.isWater = True
		elif typeFlag == 'volcano':
			self.isVolcano = True
			imgWH = (radius * 2.6, radius * 2.6)
		elif typeFlag == 'lava':
			self.isDeathy = True
		
		if EDITOR_ENABLED:
			self.isDeathy = False
		
		self.image.setSize(imgWH[0], imgWH[1])
	
	def update(self, scene, dt):
		self.theta += TWO_PI * self.rps * dt
	
	def render(self, cx, cy):
		self.image.blitRotation(self.x + cx, self.y + cy, self.theta)

	def saveState(self):
		return [self.x, self.y, self.radius, self.image, self.theta, self.rps, self.gravity, self.isWater, self.isVolcano, self.id, self.isDeathy, self.type, self.rotRat]
		
	def restoreState(self, state):
		self.x = state[0]
		self.y = state[1]
		self.radius = state[2]
		self.image = state[3]
		self.theta = state[4]
		self.rps = state[5]
		self.gravity = state[6]
		self.isWater = state[7]
		self.isVolcano = state[8]
		self.id = state[9]
		self.isDeathy = state[10]
		self.type = state[11]
		self.rotRat = state[12]