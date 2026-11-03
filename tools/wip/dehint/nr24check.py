"""One-axis rows of gen_nr24: each row differs from base in a single axis."""
import os, sys, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nrsweep, gen_nr24
out = os.path.join(nrsweep.ROOT, 'build', 'nr', 'nr24check')
os.makedirs(out, exist_ok=True)
items = []
for tag, s in gen_nr24.variants():
    p = tag.split('|')
    if sum(x != 'base' for x in p[1:]) <= 1:
        items.append((tag, s, os.path.join(out, 'v%d.c' % len(items)), []))
with cf.ThreadPoolExecutor(os.cpu_count() or 4) as ex:
    for r in ex.map(nrsweep.run, items):
        print('V=%s C=%s r=%s %s' % (r[1], r[2], r[7:], r[3]))
