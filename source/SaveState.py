class SaveState:
	def __init__(self, playscene):
		self.bodies = []
		self.sprites = []
		
		bodiesToId = {}
		
		for body in playscene.bodies:
			data = [
				body.x,
				body.y,
				body.radius,
				
			]