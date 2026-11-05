"""optr4.py REFTAG TAG [shift_from shift]: trace list of TAG beside REFTAG's (build/v/aio_p1/<tag>/aio.bbro),
ids of TAG mapped onto REFTAG's by +shift for ids >= shift_from (blocks after the xellbutton site).
Prints each trace as head[freq] with its round, side by side, and marks differences."""
import re, sys, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'build', 'v', 'aio_p1')


def traces(tag):
    t = open(os.path.join(R, tag, 'aio.bbro')).read()
    return [(int(m.group(2)), [(int(b), int(f)) for b, f in re.findall(r'(\d+) \[(\d+)\]', m.group(3))])
            for m in re.finditer(r'^Trace (\d+) \(round (\d+)\):\s+(.*)$', t, re.M)]


a = traces(sys.argv[1])
b = traces(sys.argv[2])
sf = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
sh = int(sys.argv[4]) if len(sys.argv) > 4 else 0
mp = lambda x: x + sh if x >= sf else x
fa = ['%d:%s' % (r, ' '.join('%d[%d]' % (x, f) for x, f in l)) for r, l in a]
fb = ['%d:%s' % (r, ' '.join('%d[%d]' % (mp(x), f) for x, f in l)) for r, l in b]
import difflib
for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, fa, fb, autojunk=False).get_opcodes():
    if op == 'equal':
        print('  = %d traces' % (i2 - i1))
        continue
    for x in fa[i1:i2]:
        print('-', x)
    for x in fb[j1:j2]:
        print('+', x)
