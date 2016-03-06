class GfxText:
	def __init__(self, text, size, x, y):
		self.text = text
		self.size = size
		self.x = x
		self.y = y
		self.label = None
		self.dead = False
		self.obj = None
		self.invalid = True
	
	def render(self):
		if self.invalid:
			size = Q._FONT_SIZE_BY_SHIRT[self.size]
			y = self.y - size
			self.obj = Q.pyglet.text.Label(self.text, font_name = 'Arial', font_size = size, x = self.x, y = Q.height - y, anchor_x = 'left', anchor_y = 'top')
			self.invalid = False
		self.obj.draw()
	
	def setPosition(self, x, y):
		if self.x != x or self.y != y:
			self.x = x
			self.y = y
			self.invalid = True