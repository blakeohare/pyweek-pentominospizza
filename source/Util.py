def formatTime(amount):
	if amount == None: return None
	
	deci = (int(amount * 100) % 100) / 100.0
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

def ensureLength(n, pad):
	if pad and n < 10: return '0' + str(n)
	return str(n)

def nstr(value):
	if value == None: return None
	return str(value)