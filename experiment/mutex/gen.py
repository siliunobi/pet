import sys
FILE=sys.argv[1]
OUT=sys.argv[2]
NODE=int(sys.argv[3])
BIAS=float(sys.argv[4])

file1 = open(FILE)
s = file1.read()
file1.close()
s = s.replace("$1", str(NODE))
s = s.replace("$2", str(BIAS))

file2 = open(OUT, "w")
file2.write(s)
file2.close()
