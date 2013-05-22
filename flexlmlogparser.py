'''

FLEXLMLOGPARSER
===============

VERSION
-------

1.2
  add user name in csv file

1.1
  init

'''

import sys
import re
import time

usage_top_old  = 0
usage          = 0
usage_top      = 0
out_of_license = 0
queued         = 0
user_name      = ''


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
        if re.search('TIMESTAMP',line):
            print line,

        if re.search('OUT: "' + feature + '"', line):
            usage     += 1
            user_name += ", " + re.search('OUT: "' + feature + '" (.*)  ', line).group(1)

        if re.search('IN: "' + feature + '"', line):
            usage     -= 1
            sub_name   = ", " + re.search('IN: "' + feature + '" (.*)  ', line).group(1)
            user_name  = user_name.replace(sub_name , '', 1)

        if re.search('DENIED: "' + feature + '" .* already reached', line):
            out_of_license += 1

        if re.search('QUEUED: "' + feature + '"', line):
            queued += 1

        if usage != usage_top_old:
            usage_top_old = usage # sync
            cvsfile.write("\"" + `usage` + "\",\"" + re.sub('^, ', '', user_name) + "\"\n")

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
