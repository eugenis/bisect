#!/usr/bin/python

import argparse
import subprocess

parser = argparse.ArgumentParser(description='Bisect something.')
parser.add_argument('--good', type=int)
parser.add_argument('--bad', type=int)
parser.add_argument('zz', type=str, nargs='+')

args = parser.parse_args()


good = args.good
bad = args.bad
assert good < bad
while bad - good > 1:
    mid = (good + bad) / 2
    print 'Trying %d...' % (mid, )
    log_out = open('rev%d.stdout' % (mid, ), 'w')
    log_err = open('rev%d.stderr' % (mid, ), 'w')
    ret = subprocess.call(args.zz + [str(mid)], stdout=log_out, stderr=log_err)
    if ret == 0:
        print '  ... good'
        good = mid
    else:
        print '  ... bad'
        bad = mid

print 'First bad revision:', bad
print 'Done.'
