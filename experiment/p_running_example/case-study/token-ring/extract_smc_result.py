import sys

def get_number(line):
	return float(line.split(":")[1].strip())

OUTFILE = "smc-result.txt"

if len(sys.argv) < 2:
	print("Please pass the input file as argument")
	sys.exist(0)

input_file = sys.argv[1]

alpha = None
delta = None
samples = None
result = None
run_time = None

for line in open(input_file).readlines():
	if line.startswith("alpha:"):
		alpha = get_number(line)
	elif line.startswith("delta1:"):
		delta = get_number(line)
	elif line.startswith("samples generated"):
		samples = int(line.split("=")[1].strip())
	elif line.startswith("Result:"):
		result = get_number(line)
	elif line.startswith("Running time:"):
		run_time = float(line.split(":")[1].strip().split(" ")[0])


f = open(OUTFILE, "w")
f.write("Confidence (alpha): %s\n" % alpha)
f.write("Threshold (delta): %s\n" % delta)
f.write("Samples generated: %s\n" % samples)
f.write("Result: %s\n" % result)
f.write("Running time: %s seconds\n" % run_time)
f.close()

