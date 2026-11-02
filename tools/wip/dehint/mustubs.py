"""Blocks bb-reorder pops, with frequencies: python mustubs.py <bbro.txt>
Needs -fdump-rtl-bbro-details-blocks, cut to one function (mufn.py)."""
import re, sys
t = open(sys.argv[1]).read()
t = t[t.index('Reordering with the STC'):]
head, tail = t, t
freq = {}
all_t = open(sys.argv[1]).read()
for m in re.finditer(r'^basic block (\d+), loop depth \d+, count \d+, freq (\d+)', all_t, re.M):
    freq.setdefault(m.group(1), m.group(2))
order = re.findall(r'Getting bb (\d+)|(STC - round \d)', t)
print(' '.join('[%s]' % r[-1] if r else '%s:%s' % (b, freq.get(b, '?')) for b, r in order))
