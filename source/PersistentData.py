INT = type(42)
FLOAT = type(42.5)
STRING = type('42')
BOOL = type(True)

class PersistentData:
	def __init__(self):
		self.values = {}
		self.folder = '.'
		self.filename = 'pp_save_data.txt'
		self.initialize() # sets the save file or doesn't if it can't figure out the system.
	
	def initialize(self):
		if os.name == 'nt':
			appdata = os.environ.get('APPDATA')
			if appdata != None:
				self.folder = os.path.join(appdata, 'PentominosPizza')
		elif os.sys.platform.startswith('linux') or os.name == 'os2':
			if os.path.exists('~') and os.path.isdir('~'):
				self.folder = os.path.join('~', '.pentominospizza')
		else:
			pass # just leave as '.'
		
		if self.folder != '.' and not os.path.exists(self.folder):
			try:
				os.makedirs(self.folder)
			except:
				print("persistent file creation failed")
				self.folder = '.'
				self.initialize()
				return
		
		path = os.path.join(self.folder, self.filename)
		data = ''
		if os.path.exists(path):
			try:
				c = open(path, 'rt')
				data = c.read()
				c.close()
			except:
				data = ''
		
		for line in data.split('\n'):
			line = line.strip()
			if len(line) > 0:
				parts = line.split(':')
				if len(parts) >= 3:
					t = parts[0].upper().strip()
					k = parts[1].strip()
					v = ':'.join(parts[2:]).strip()
					if t == 'I':
						try:
							v = int(v)
						except:
							k = None
					elif t == 'F':
						try:
							v = float(v)
						except:
							k = None
					elif t == 'B':
						v = v == '1'
					elif t == 'S':
						pass
					elif t == 'N':
						v = None
					else:
						k = None
					if k != None:
						self.values[k] = v
	
	def save(self):
		if self.folder == None: return
		output = []
		for key in self.values.keys():
			t = None
			value = self.values[key]
			ktype = type(value)
			if ktype == INT:
				t = 'I'
			elif ktype == STRING:
				t = 'S'
			elif ktype == BOOL:
				t = 'B'
				value = 1 if value else 0
			elif ktype == FLOAT:
				t = 'F'
			elif value == None:
				t = 'N'
				value = '-'
			output.append(t + ':' + key + ':' + str(value))
		
		try:
			c = open(os.path.join(self.folder, self.filename), 'wt')
			c.write('\n'.join(output))
			c.close()
		except:
			print("Persistent file write failed.")
			pass
	
	def getValue(self, key, default):
		return self.values.get(key, default)
	
	def setValue(self, key, value):
		self.values[key] = value

DB = PersistentData()