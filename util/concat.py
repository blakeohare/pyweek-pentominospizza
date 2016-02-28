import os

def get_all_py_files(dir, output):
	for file in os.listdir(dir):
		full = dir + os.sep + file
		if os.path.isdir(full):
			get_all_py_files(full, output)
		elif full.endswith('.py'):
			c = open(full, 'rt')
			t = c.read()
			c.close()
			output[full.replace('\\', '/')] = t


files = {}
get_all_py_files(os.path.join('.', 'source'), files)

names = list(files.keys())

output = []
names.sort()

output.append(files['./source/header.py'])

for name in names:
	if name != './source/header.py' and name != './source/main.py':
		output.append('\n')
		output.append(files[name])
		output.append('\n')

output.append(files['./source/main.py'])

c = open('run.py', 'wt')
c.write('\n'.join(output))
c.close()
