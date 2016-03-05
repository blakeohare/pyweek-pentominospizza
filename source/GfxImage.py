_GFX_IMAGE_LIBRARY = {}

class RawImage:
	def __init__(self, resource):
		self.resource = resource
		# original width and height
		self.width = resource.width
		self.height = resource.height
		self.cx = self.width // 2
		self.cy = self.height // 2
		self.centered = False
		self.anchor_x = 0
		self.anchor_y = 0
	
	def anchorTopLeft(self):
		if self.centered:
			self.centered = False
			self.resource.anchor_x = 0
			self.resource.anchor_y = 0
	
	def anchorCenter(self):
		if not self.centered:
			self.centered = True
			self.resource.anchor_x = self.cx
			self.resource.anchor_y = self.cy


class GfxImage:
	def __init__(self, path):
		img = _GFX_IMAGE_LIBRARY.get(path)
		if img == None:
			img = RawImage(Q.pyglet.resource.image(os.path.join('images', path.replace('/', os.sep)).replace('\\', '/')))
			_GFX_IMAGE_LIBRARY[path] = img
		self.img = img
		self.sprite = Q.pyglet.sprite.Sprite(img.resource)
		self.centered = False
		self.sprite.anchor_x = 0
		self.sprite.anchor_y = 0
		self.width = img.width
		self.height = img.height
		self.theta = None
	
	def setSize(self, width, height):
		self.width = width
		self.height = height
		self.sprite.image.width = width
		self.sprite.image.height = height
		self.centered = False
		self.sprite.anchor_x = 0
		self.sprite.anchor_y = 0
		self.img.cx = width / 2.0
		self.img.cy = height / 2.0
		
	def blitSimple(self, x, y):
		self.img.anchorTopLeft()
		if self.theta != None:
			self.sprite.rotation = 0
			self.theta = None
		self.sprite.x = x
		self.sprite.y = Q.height - y - self.height
		if self.centered:
			self.centered = False
			self.sprite.anchor_x = 0
			self.sprite.anchor_y = 0
		
		self.sprite.draw()
	
	def blitRotation(self, x, y, theta):
		self.img.anchorCenter()
		if self.theta == None: self.theta = 0
		diff = theta - self.theta
		if diff < -0.00001 or diff > 0.00001:
			self.theta = theta
			self.sprite.rotation = 360 / TWO_PI * theta + 90
		
		ry = Q.height - y
		
		self.sprite.set_position(x, ry)
		self.sprite.draw()	
	