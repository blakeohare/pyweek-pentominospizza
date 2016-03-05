def formatTime(amount):
	if amount == None: return None
	
	deci = int(amount * 100) % 100
	amount = int(amount)
	seconds = amount % 60
	amount = amount / 60
	minutes = amount % 60
	hours = amount / 60
	
	if hours > 0:
		return ':'.join((ensureLength(hours, False), ensureLength(minutes, True), ensureLength(seconds, True) + '.' + ensureLength(deci, True)))
	
	if minutes > 0:
		return ''.join((ensureLength(minutes, False), "' ", ensureLength(seconds, True), '.', ensureLength(deci, True), '"'))
	
	return ensureLength(seconds, False) + "." + ensureLength(deci, True) + '"'

def formatCountdown(seconds):
	minutes = seconds // 60
	seconds = seconds % 60
	if seconds < 10:
		return str(minutes) + ':0' + str(seconds)
	return str(minutes) + ':' + str(seconds)
	
def ensureLength(n, pad):
	if pad and n < 10: return '0' + str(n)
	return str(n)

def nstr(value):
	if value == None: return None
	return str(value)

def safeTan(ang):
	s = math.sin(ang)
	c = math.cos(ang)
	if abs(c) < .00001:
		return 999999999
	return s / c
	
def findIntersectionOrNull(angle, ax, ay, bx, by, dist):
	cx = math.cos(angle) * 500
	cy = math.sin(angle) * 500
	
	if ax == bx :#and abs(cx) * 2 > abs(cy):
		y = safeTan(angle) * abs(ax)
		if ax < 0: y = -y
		if ay > by:
			ay, by = by, ay
		
		if y > ay and y < by:
			if (ax < 0) == (cx < 0):
				if (ax ** 2) + y ** 2 < dist ** 2:
					return (ax, y)
	
	if ay == by :#and abs(cx) > abs(cy) * 2:
		x = abs(ay) / safeTan(angle)
		if ay < 0: x = -x
		if ax > bx:
			ax, by = bx, by
		
		
		
		if x > ax and x < bx:
			if (ay < 0) == (cy < 0):
				if (ay ** 2) + x ** 2 < dist ** 2:
					return (x, ay)
	
	return None
