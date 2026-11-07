"""Attempt 55: print loadBlFiles' r = 1 block (movl $1,%edi) and arm 1's retest block from -dA output.
python tools/wip/dehint/bdgen/a55_r1.py <variant.c>... (p99)"""
import os, re, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bdlib
for f in sys.argv[1:]:
    ok, o, d = bdlib.compile_src(open(f, newline='').read(), bdlib.P98, asm=True, extra=['-dA'])
    if not ok:
        print(f, 'ERR', o[:300]); continue
    t = open(o).read(); i = t.index('_loadBlFiles:'); j = t.index('.def', i); s = t[i:j]
    bl = re.split(r'\n(?= # BLOCK )', s)
    out = []
    for k, b in enumerate(bl):
        m = re.match(r' # BLOCK (\d+)(?: freq:(\d+))? seq:(\d+)', b)
        if not m: continue
        if 'movl\t$1, %edi' in b or ('subl\t$4' in b and 'call' not in b) or '_suGetCF' in b or 'call\t_malloc' in b:
            pred = re.search(r'# PRED: ([^\n]*)', b).group(1).strip()
            tag = 'R1' if 'movl\t$1, %edi' in b else 'SUB' if 'subl\t$4' in b else 'CF' if '_suGetCF' in b else 'MAL'
            out.append('%s bb%s f%s seq%s <- %s' % (tag, m.group(1), m.group(2) or 0, m.group(3), re.sub(r'\s*\([A-Z_,]+\)', '', pred)))
    print('==', os.path.basename(f)); print('\n'.join(out))
    bdlib.cleanup(d)
