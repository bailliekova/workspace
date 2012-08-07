import sys
from datetime import datetime as dt

infile= open(sys.argv[1], "r")
outfile= open(sys.argv[2], "a")
n=1

for line in infile:
    print line
    tokens=line.split("\t")
    if n<4:
        n+=1
        continue
    olddate=tokens[3]
    print tokens[0]
    print tokens[1]
    print tokens[2]
    print tokens[3]
    print "Datetime is: " + olddate
    isodate=dt.strptime(olddate, "%d %b %Y %H:%M:%S %Z").isoformat()[:10]
    outfile.write("\t".join([isodate, str(n-3), tokens[1], tokens[10], tokens[14], tokens[2], tokens[16]]) + "\n")
    outfile.flush()
    n+=1
outfile.close()
infile.close()
