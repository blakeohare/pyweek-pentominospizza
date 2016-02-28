class ImageLibrary:
	def __init__(self):
		self.images = {}
	
	def get(self, path):
		img = self.images.get(path)
		if img == null:
			img = pygame.image.load(('source/images/' + path).replace('/', os.sep))
			self.images[path] = img
		return img

IMAGES = ImageLibrary()
