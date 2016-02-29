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
			if len(line) > 0:
				if line[0] != '+':
					parts = line.split(',')
					objectId = parts[0].strip()
					x = int(parts[1].strip())
					y = int(parts[2].strip())
					activeObject = (objectId, x, y, [])
					objects.append(activeObject)
				else:
					parts = line[1:].split(',')
					spriteId = parts[0].strip()
					theta = int(parts[1].strip()[1:]) * 2 * 3.14159265358979  / 360
					activeObject[3].append((spriteId, theta))
		
		self.stuff = objects