class Level:
	def __init__(self, id):
		self.id = id
		objects = []
		c = open(os.path.join('source', 'levels', id + '.txt'), 'rt')
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