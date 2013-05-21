'''
version 1.1
'''

import sys
import re
import time

usage_top_old  = 0
usage          = 0
usage_top      = 0
out_of_license = 0
queued         = 0
#user_name      = ''


if len(sys.argv) < 4:
    print "USAGE: flexlmlogparser feature input.log output.csv"
    exit(1)

feature =  sys.argv[1]
cvsfile = open(sys.argv[3], 'w+')

print "FEATURE: " + feature
print "COUTING... please wait"
time.sleep(1)

with open(sys.argv[2], 'r') as f:
    for line in f:
        m = re.search('TIMESTAMP',line)
        if m:
            print line,

        m = re.search('OUT: "' + feature + '"', line)
        if m:
            usage     += 1
            #user_name += re.search('OUT: "' + feature + '" (.*)', line).group(1)

        m = re.search('IN: "' + feature + '"', line)
        if m:
            usage    -= 1
            #sub_name  = re.search('IN: "' + feature + '" (.*)', line).group(1)
            #user_name = re.sub(sub_name , '', user_name)

        m = re.search('DENIED: "' + feature + '" .* already reached', line)
        if m:
            out_of_license += 1

        m = re.search('QUEUED: "' + feature + '"', line)
        if m:
            queued += 1

        if usage != usage_top_old:
            usage_top_old = usage # sync
            cvsfile.write(`usage`+"\n")

        if usage >= usage_top:
            usage_top = usage

cvsfile.close()

print "\n\n"
print "**********************************************"
print "Report:"
print "    Max usage         = " + `usage_top`
print "    License Runs out  = " + `out_of_license`
print "    Queued            = " + `queued`
print "**********************************************"
