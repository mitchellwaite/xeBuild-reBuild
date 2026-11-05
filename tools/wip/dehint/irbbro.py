"""python tools/wip/dehint/irbbro.py <file.c> <fn> [dump]: per-block frequencies of <fn> from the bbro dump (or the named RTL dump's
last listing), blocks in layout order with preds/succs and their %, plus .p2align placements from -S.  For compute_alignments questions:
a block with a fallthru is aligned when branch_freq > fallthru_freq * align-loop-iterations (4) and their sum > max_freq / 100; without, when branch > threshold."""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib

src, fn = sys.argv[1:3]
text = open(src, newline='').read().replace('\r\n', '\n')
ok, o, d = irlib.compile_src(text, [], extra=['-fdump-rtl-bbro-blocks-details', '-dp'])
if not ok:
    print(o)
    sys.exit(1)
f = [x for x in os.listdir(d) if x.endswith('bbro')][0]
t = open(os.path.join(d, f), errors='replace').read()
t = t[t.find(';; Function ' + fn):]
t = t[:t.find(';; Function', 10)]
# the last listing: everything after the final "Duplicated" or the trace dump
i = t.rfind('Reorder')
for m in re.finditer(r';; basic block (\d+), loop depth \d+, count \d+, freq (\d+)[^\n]*\n((?:;;[^\n]*\n)*)', t):
    pr = re.findall(r';;\s+(?:pred:|succ:)?\s*(\d+|ENTRY|EXIT) \[([\d.]+)%\]( \([^)]*\))?', m.group(3))
    print('bb%-3s f=%-6s %s' % (m.group(1), m.group(2), ' '.join('%s[%s]%s' % (a, b, 'ft' if 'FALLTHRU' in c else '') for a, b, c in pr)))
irlib.cleanup(d)
