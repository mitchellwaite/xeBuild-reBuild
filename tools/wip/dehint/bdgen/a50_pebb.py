"""Attempt 50: python tools/wip/dehint/bdgen/a50_pebb.py <dump.profile_estimate> [fn]
One line per bb of fn's body at profile_estimate (the second ';; Function fn' listing):
bb, frequency, and its calls / conditions / constant stores, so two sources' profiles can be lined up."""
import re, sys

t = open(sys.argv[1], errors='replace').read()
fn = sys.argv[2] if len(sys.argv) > 2 else 'loadBlFiles'
starts = [m.start() for m in re.finditer(r'^;; Function %s ' % re.escape(fn), t, re.M)]
s = starts[-1]
e = t.find('\n;; Function ', s + 10)
body = t[s:e if e > 0 else None]
cur = None
rows = []
for l in body.splitlines():
    m = re.match(r'\s*;;\s+basic block (\d+), loop depth (\d+), count \d+, freq (\d+)', l)
    if m:
        cur = [int(m.group(1)), int(m.group(3)), []]
        rows.append(cur)
        continue
    if cur is None:
        continue
    l2 = l.strip()
    if re.match(r'^(if \(|switch|[\w.]+ = \w+ \(|\w+ \()', l2) or ('= ' in l2 and re.search(r'= -?\d+;$', l2)) or 'log_printf' in l2:
        x = re.sub(r'<[^>]*>', '', l2)
        cur[2].append(x[:60])
for b, f, xs in rows:
    print('bb %-4d %5d  %s' % (b, f, ' | '.join(xs)))
