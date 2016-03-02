'''
data saved:
boolean -> intro_shown

boolean -> {map key}_completed
float -> {map_key}_longestjump (seconds)
float -> {map_key}_fastesttime (seconds)
int -> {map_key}_fewestjumps
int -> {map_key}_timesplayed

A map is considered unlocked if it is first in the manifest or its previous map is marked as _completed

'''

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
	
	def getBoolean(self, key, default = False):
		return self.values.get(key, default) == True
	
	def getFloat(self, key, default = 0.0):
		output = self.values.get(key, default)
		if type(output) == FLOAT:
			return output
		if type(output) == INT:
			return output + 0.0
		return default
	
	def getInteger(self, key, default = 0):
		return self.getInt(key, default)
	
	def getInt(self, key, default = 0):
		output = self.values.get(key, default)
		if type(output) == INT:
			return output
		if type(output) == FLOAT:
			return int(output)
		return default
	
	def getString(self, key, default = None):
		return str(self.values.get(key, default))
	
	def hasValue(self, key):
		return key in self.values
	
	def setValue(self, key, value):
		self.values[key] = value

DB = PersistentData()