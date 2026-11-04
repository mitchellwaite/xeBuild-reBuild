"""python tools/wip/dehint/iw9exp.py <base.c>: experiment for pin_hdr's mechanism.  __builtin_expect on the ECC test
in finalizeImage with --param builtin-expect-probability=N for N in a grid, pin removed: does the head block's frequency
alone (r201's spill priority) give the reference's allocation?  Not a source candidate, only a test of the mechanism."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib

PIN = '__asm__("" :: "a"(xb.hdr));'
IF = 'if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))'
EX = 'if (__builtin_expect(!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16), 0))'
t = open(sys.argv[1], newline='').read().replace('\r\n', '\n')
assert IF in t
t = t.replace(IF, EX)
t = t.replace('\t\t\t' + PIN + '\n', '')
for n in (50, 55, 60, 65, 70, 72, 75, 78, 80, 82, 85, 88, 90, 92, 95, 97, 99, 100):
    r = iwlib.score_text(t, ['--param', 'builtin-expect-probability=%d' % n])
    print(n, iwlib.fmt(r))
