"""python tools/wip/dehint/irfqp.py <file.c> '<old>' '<new with __builtin_expect>' p1 p2 ... : measurement only: how far must one test's probability move for
parseDump's entry frequency to change?  Prints entry, tail, parseDump's diff size at each builtin-expect-probability."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib

src, old, new = sys.argv[1:4]
text = open(src, newline='').read().replace('\r\n', '\n')
assert old in text
text = text.replace(old, new)
for p in sys.argv[4:]:
    ok, o, d = irlib.compile_src(text, ['--param', 'builtin-expect-probability=' + p], extra=['-fdump-tree-optimized-blocks-details'])
    if not ok:
        print(o)
        break
    idn, tot, per, notes = irlib.report(o)
    f = [x for x in os.listdir(d) if x.endswith('optimized')]
    txt = open(os.path.join(d, f[0]), errors='replace').read()
    irlib.cleanup(d)
    txt = txt[txt.find(';; Function parseDump'):]
    txt = txt[:txt.find(';; Function', 10)]
    entry = tail = cur = None
    for line in txt.split('\n'):
        m = re.match(r';;\s+basic block (\d+), loop depth \d+, count \d+, freq (\d+)', line)
        if m:
            cur = int(m.group(2))
            if m.group(1) == '2':
                entry = cur
        if '-----------------' in line:
            tail = cur
    print(p, 'entry', entry, 'tail', tail, 'IDENTICAL' if idn else per.get('_parseDump'), flush=True)
