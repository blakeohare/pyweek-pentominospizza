
def main():
	
	pygame.init()
	
	screen = pygame.display.set_mode((800, 600))
	is_fullscreen = False
	
	scene = TitleScene()
	rc = 0
	events = []
	pressed_keys = {}
	while True:
		start = time.time()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			
			if event.type == pygame.KEYDOWN:
				pressed_keys[event.key] = True
				if event.key == pygame.K_F4 and (pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]):
					return
				
				if event.key == pygame.K_p:
					if is_fullscreen:
						screen = pygame.display.set_mode((800, 600))
					else:
						screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
					is_fullscreen = not is_fullscreen
						
			if event.type == pygame.KEYUP:
				pressed_keys[event.key] = False
		
		scene.update(events, pressed_keys)
		scene.render(screen, rc)
		rc += 1
		pygame.display.flip()
		end = time.time()
		diff = end - start
		delay = 1 / 30.0 - diff
		if delay > 0:
			time.sleep(delay)
			
main()
