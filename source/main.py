
def main():
	
	Q.openWindow('Space game of some sort', 800, 600)
	
	scene = TitleScene()
	rc = 0
	while True:
		events = Q.pumpEvents()
		if Q.exitGame:
			return
		
		scene.update(events)
		
		if scene != scene.next:
			old = scene
			scene = scene.next
			old.next = None
		
		scene.render(rc)
		rc += 1
		
		Q.clockTick()
		
			
main()
