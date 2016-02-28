FONTS_SIZE_BY_TSHIRT = {
	'XL': 36,
	'L': 20,
	'M': 16,
	'S': 12,
}

LETTERS = 'abcdefghijklmnopqrstuvwxyz'
LETTERS += LETTERS.upper()
LETTERS += '0123456789'
LETTERS += '!@#$%^&*`~()-_=+[]{}|\\;:\'",.<>?/'


class FontEngine:
	def __init__(self):
		self.characters_by_size = {}
	

	def render(self, screen, text, size, x, y):
		size_set = self.characters_by_size.get(size)
		if size_set == None:
			size_set = {}
			font = pygame.font.Font('source' + os.sep + 'fonts' + os.sep + 'orena.ttf', FONTS_SIZE_BY_TSHIRT[size.upper()])
			for letter in LETTERS:
				size_set[letter] = font.render(letter, True, (255, 255, 255))
			self.characters_by_size[size] = size_set
		
		for c in text:
			if c == ' ':
				x += size_set['v'].get_width()
			else:
				letter = size_set.get(c, '?')
				screen.blit(letter, (x, y))
				x += letter.get_width()
				

FONT = FontEngine()