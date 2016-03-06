class MapMetadata:
	def __init__(self, key, name):
		self.key = key
		self.name = name
		self.next = None
		
class MapDatabase:
	def __init__(self):
		self.values = {}
		self.order = []
		
		c = open(os.path.join('source', 'levels', 'manifest.txt'), 'rt')
		lines = c.read().split('\n')
		c.close()
		
		prev = None
		for line in lines:
			parts = line.split(':')
			if len(parts) == 2:
				key = parts[0].strip()
				name = parts[1].strip()
				metadata = MapMetadata(key, name)
				metadata.prev = prev
				if prev != None:
					prev.next = metadata
				prev = metadata
		
				self.order.append(key)
				self.values[key] = metadata
	
	def get(self, key):
		return self.values.get(key)
	
	def getKeys(self):
		return self.order[:]
	
	def isUnlocked(self, key):
		if self.order[0] == key: return True
		m = self.get(key)
		if m == None: return False
		key = m.prev.key
		return DB.getBoolean(key + '_completed')

MAP_DB = MapDatabase()