import os
import sys

INPUT_FOLDER = "input-modules"

def replace_str(src, old, new):
	content = open(src).read()
	content = content.replace(old, new)
	with open(src, "w") as f:
		f.write(content)

def get_file_name(name, is_upper=False):
	name = name.split(".")[0]
	return name.upper() if is_upper else name

def save_lines(dst, lines, end_line=False):
	with open(dst, "w") as f:
		for line in lines:
			if end_line:
				f.write("%s\n" % line)
			else:
				f.write("%s" % line)

def copy_file(src, dst):
	dst_dir = os.path.dirname(dst)
	if not os.path.exists(dst_dir):
		os.makedirs(dst_dir)
	with open(src, 'r') as f:
		data = f.read()
	with open(dst, 'w') as f:
		f.write(data)

def copy_with_module_process(src, dst):
	dst_dir = os.path.dirname(dst)
	if not os.path.exists(dst_dir):
		os.makedirs(dst_dir)
	res = []
	for line in open(src).readlines():
		if line.startswith("fmod") or line.startswith("mod"):
			res.append("(%s" % line)
		elif line.startswith("endm"):
			line = line.replace("endm", "endm)")
			res.append(line)
		else:
			res.append(line)

	save_lines(dst, res)


def process_pmonitor_file(args):
	pmonitor = "full-maude/pmonitor.maude"
	lines = []
	for line in open(pmonitor).readlines():
		if line.startswith("*** scripts start here"):
			break
		lines.append(line)	
	lines.append("*** scripts start here\n\n")
	lines.append("load sampling-lib.maude\n\n")
	lines.append("load input-modules-full-maude/%s\n\n" % args[3])
	lines.append("(p-trans %s .)\n\n" % get_file_name(args[1], True))
	lines.append("(show module P-%s .)\n\n" % get_file_name(args[1], True))
	lines.append("load input-modules-full-maude/%s\n\n" % args[2])
	lines.append("(p-init %s .)\n\n" % get_file_name(args[2], True))
	lines.append("(show module P-%s .)\n\n" % get_file_name(args[2], True))
	lines.append("q\n")
	save_lines(pmonitor, lines)

def extract_module(module_name):
	res = []
	lines = open(output_file).readlines()
	i = 0
	while i < len(lines):
		line = lines[i]
		if line.startswith("mod %s is" % module_name):
			while not lines[i].startswith("endm"):
				res.append(lines[i])
				i += 1
			res.append(lines[i])
			break
		i += 1
	if len(res) == 0:
		print("Didn't find module %s" % module_name)
	return res


def replace_module(src_file, dst_file, module_name, prefix, insert_lines=[]):
	res = []
	lines = open(src_file).readlines()
	i  = 0
	while i < len(lines):
		line = lines[i]
		if line.startswith("mod %s is" % module_name):
			while not lines[i].startswith("endm"):
				i += 1			
			for line in insert_lines:
				res.append("%s\n" % line)
			for line in extract_module("%s-%s" % (prefix, module_name)):
				res.append(line)			
		else:
			res.append(line)
		i += 1
	save_lines(dst_file, res)


if __name__ == "__main__":
	
	output_file = "output"
	smc = sys.argv[2]
	app_name = get_file_name(sys.argv[4])
	if smc == "off":
		args = sys.argv[4:8]  #['query.maude', 'init-query.maude', 'pi-query.maude', 'events-query.maude']

		src = os.path.join("p-output", args[0])
		dst = os.path.join("p-output", "p-%s" % args[0])
		name = get_file_name(args[0], True)
		insert_lines = ["load %s" % get_file_name(args[2]), "load ../sampling-lib", ""]
		replace_module(src, dst, name, "P", insert_lines)
	
	
		src = os.path.join("p-output", args[1])
		dst = os.path.join("p-output", "p-%s" % args[1])
		name = get_file_name(args[1], True)
		replace_module(src, dst, name, "P")
		replace_str(dst, "load %s" % app_name, "load p-%s" % app_name)
	elif smc == "on":
		args = sys.argv[4:8]  #['query.maude', 'init-query.maude', 'pi-query.maude', 'events-query.maude']

		src = os.path.join("m-output", args[0])
		dst = os.path.join("m-output", "m-p-%s" % args[0])
		name = get_file_name(args[0], True)
		insert_lines = ["load %s" % get_file_name(args[2]), "load ../sampling-lib", "load events-%s" % app_name]
		replace_module(src, dst, name, "M-P", insert_lines)
	
	
		src = os.path.join("m-output", args[1])
		dst = os.path.join("m-output", "m-p-%s" % args[1])
		name = get_file_name(args[1], True)
		replace_module(src, dst, name, "M-P")
		replace_str(dst, "load %s" % get_file_name(args[0]), "load m-p-%s" % get_file_name(args[0]))
					
	
