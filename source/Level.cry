class Level:
	def __init__(self, id):
		self.id = id
		objects = []
		path = os.path.join('source', 'levels', id + '.txt')
		c = open(path, 'rt')
		lines = c.read().split('\n')
		c.close()
		activeObject = None
		for line in lines:
			line = line.strip()
			speedRatio = 1.0
			if len(line) > 0:
				if line[0] != '+':
					parts = line.split(',')
					objectId = parts[0].strip()
					x = int(parts[1].strip())
					y = int(parts[2].strip())
					if len(parts) > 3:
						speedRatio = float(parts[3].strip()) # can be negative to rotate in other direction
					activeObject = (objectId, x, y, [], speedRatio)
					objects.append(activeObject)
				else:
					parts = line[1:].split(',')
					spriteId = parts[0].strip()
					theta = int(parts[1].strip()[1:]) * TWO_PI  / 360
					
					activeObject[3].append((spriteId, theta))
		
		self.stuff = objects

# This is pretty cheesy. Since you can't add or delete asteroids in the editor or change their 
# order, take the bodies and just re-allocate them into the file. This will preserve sprite starting locations.
def saveLevel(playscene):
	bodies = playscene.bodies[:]
	path = os.path.join('source', 'levels', playscene.id + '.txt')
	c = open(path, 'rt')
	lines = c.read().split('\n')
	c.close()
	for i in range(len(lines)):
		line = lines[i].strip()
		if len(line) > 0:
			if line[0] != '+' and len(bodies) > 0:
				body = bodies[0]
				newLine = body.type + ', ' + str(int(body.x)) + ', ' + str(int(body.y)) + ', ' + str(body.rotRat)
				lines[i] = newLine
				bodies = bodies[1:]
	c = open(path, 'wt')
	c.write('\n'.join(lines))
	c.close()
	