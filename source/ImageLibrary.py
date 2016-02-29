IMAGE_ROTATION_INCREMENTS = 500

class ImageLibrary:
	def __init__(self):
		self.images = {}
		self.imagesByThetaByPath = {}
	
	def get(self, path):
		img = self.images.get(path)
		if img == None:
			img = pygame.image.load(('source/images/' + path).replace('/', os.sep))
			self.images[path] = img
		return img
	
	def getRotated(self, path, theta):
		theta = theta / TWO_PI % 1
		if theta < 0: theta += 1
		lookup = self.imagesByThetaByPath.get(path)
		if lookup == None:
			img = self.get(path)
			lookup = [img]
			self.imagesByThetaByPath[path] = lookup
			
			for i in range(1, IMAGE_ROTATION_INCREMENTS):
				t = i * 360 / IMAGE_ROTATION_INCREMENTS # degrees? really? PyGame, we need to have a talk.
				lookup.append(pygame.transform.rotate(img, t))
		
		
		return lookup[int(theta * len(lookup))]
		
		

IMAGES = ImageLibrary()
