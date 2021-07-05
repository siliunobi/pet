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
			line = "(%s" % line
		elif line.startswith("endm"):
			line = line.replace("endm", "endm)")
		elif line.startswith("endfm"):
			line = line.replace("endfm", "endfm)")
		else:
			if line.startswith("view"):
				line = "(%s" % line
			if "endv" in line:
				line = line.replace("endv", "endv)")
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
	lines.append("load input-modules-full-maude/%s\n\n" % args[2])
	lines.append("(p-trans %s .)\n\n" % get_file_name(args[0], True))
	lines.append("(show module P-%s .)\n\n" % get_file_name(args[0], True))
	lines.append("load input-modules-full-maude/%s\n\n" % args[1])
	lines.append("(p-init %s .)\n\n" % get_file_name(args[1], True))
	lines.append("(show module P-%s .)\n\n" % get_file_name(args[1], True))
	lines.append("*** scripts end here\n\n")
	lines.append("q\n")
	save_lines(pmonitor, lines)

def add_to_pmonitor_file(args):
	pmonitor = "full-maude/pmonitor.maude"
	lines = []
	for line in open(pmonitor).readlines():
		if line.startswith("*** scripts end here"):
			lines.append(line)
			break
		lines.append(line)	
	lines.append("load input-modules-full-maude/%s\n\n" % args[3])
	lines.append("(pm-trans %s .)\n\n" % get_file_name(args[0], True))
	lines.append("(show module M-P-%s .)\n\n" % get_file_name(args[0], True))
	lines.append("(pm-init %s .)\n\n" % get_file_name(args[1], True))
	lines.append("(show module M-P-%s .)\n\n" % get_file_name(args[1], True))
	
	lines.append("q\n")
	save_lines(pmonitor, lines)

if __name__ == "__main__":
	smc = sys.argv[2]
	app_name = get_file_name(sys.argv[4])
	if smc == "off":
		args = sys.argv[4:8]  #['query.maude', 'init-query.maude', 'pi-query.maude', 'events-query.maude']

		output_dir = "p-output"
		for i in range(len(args)):
			src = os.path.join(INPUT_FOLDER, args[i])
			dst = os.path.join(output_dir, args[i])
			copy_file(src, dst)

			
		output_dir = "full-maude/input-modules-full-maude"
		for i in range(len(args)):
			src = os.path.join(INPUT_FOLDER, args[i])
			dst = os.path.join(output_dir, args[i])
			copy_with_module_process(src, dst)
			if args[i].startswith("events-"):
				replace_str(dst, "load %s" % app_name, "***load %s" % app_name)

		process_pmonitor_file(args)
	elif smc == "on":
		args = sys.argv[4:8]  #['query.maude', 'init-query.maude', 'pi-query.maude', 'events-query.maude']
		output_dir = "m-output"
		for i in range(len(args)):
			src = os.path.join(INPUT_FOLDER, args[i])
			dst = os.path.join(output_dir, args[i])
			copy_file(src, dst)
			
		output_dir = "full-maude/input-modules-full-maude"
		for i in range(len(args)):
			src = os.path.join(INPUT_FOLDER, args[i])
			dst = os.path.join(output_dir, args[i])
			copy_with_module_process(src, dst)
			if i == len(args)-1:
				replace_str(dst, "load %s" % app_name, "***load %s" % app_name)
		
		add_to_pmonitor_file(args)
		
