import sys

TOTAL=200
FILE=sys.argv[1]
OUT=sys.argv[2]
RC=int(sys.argv[3])
WC=TOTAL-RC
CLASSES=int(sys.argv[4])
READ_LEVEL=sys.argv[5]

file1 = open(FILE)
s = file1.read()
file1.close()
s = s.replace("$1", str(RC))
s = s.replace("$2", str(WC))
s = s.replace("$3", str(CLASSES))
s = s.replace("$4", str(READ_LEVEL))

file2 = open(OUT, "w")
file2.write(s)
file2.close()
