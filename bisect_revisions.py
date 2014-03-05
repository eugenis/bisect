#!/usr/bin/python

import argparse
import subprocess
import sys

failed = set()

def pick_next_revision(good, bad):
    r = (good + bad) / 2
    if r not in failed:
        return r
    for d in range(1, (bad - good) / 2):
        if (r + d) not in failed:
            return r + d
        if (r - d) not in failed:
            return r - d
    print "No valid revisions left!"
    print "good: %d, bad: %d" % (good, bad)
    print "Done."
    sys.exit(0)


parser = argparse.ArgumentParser(description='Bisect something.')
parser.add_argument('--good', type=int)
parser.add_argument('--bad', type=int)
parser.add_argument('zz', type=str, nargs='+')

args = parser.parse_args()

good = args.good
bad = args.bad
assert good < bad
while bad - good > 1:
    mid = pick_next_revision(good, bad)
    print 'Trying %d...' % (mid, )
    log_out = open('rev%d.stdout' % (mid, ), 'w')
    log_err = open('rev%d.stderr' % (mid, ), 'w')
    ret = subprocess.call(args.zz + [str(mid)], stdout=log_out, stderr=log_err)
    print ret
    if ret == 0:
        print '  ... good'
        good = mid
    elif ret == 42:
        print ' ... failed'
        failed.add(mid)
    else:
        print '  ... bad'
        bad = mid

print 'First bad revision:', bad
print 'Done.'
