
def main():
	if DB.getBoolean('intro_shown'):
		start = TitleScene()
	else:
		start = CutScene()
	Q.openWindow("Pentomino's Pizza", 800, 600, start)
	
main()
