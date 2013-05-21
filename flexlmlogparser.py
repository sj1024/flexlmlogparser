'''
version 1.1
'''

import sys
import re
import time

usage_old = 0
usage = 0


if len(sys.argv) < 4:
    print "USAGE: flexlmlogparser feature input.log output.csv"
    exit(1)

feature =  sys.argv[1]
cvsfile = open(sys.argv[3], 'w+')

print "FEATURE: "+feature
print "COUTING... please wait"
time.sleep(1)

with open(sys.argv[2], 'r') as f:
    for line in f:

        m = re.search('OUT: "'+feature+'"', line)
        if m:
            usage += 1

        m = re.search('IN: "'+feature+'"', line)
        if m:
            usage -= 1

        if usage != usage_old:
            usage_old = usage # sync
            cvsfile.write(`usage`+"\n")
            print usage,

cvsfile.close()

