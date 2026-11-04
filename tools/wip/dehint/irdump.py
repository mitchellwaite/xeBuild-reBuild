"""python tools/wip/dehint/irdump.py <file.c> <outdir> <fn> [dumpflag ...]
Compile <file.c> as build.sh does with the given -fdump flags (default tree-all-details,
rtl-ce1, rtl-bbro) and write only function <fn>'s part of every dump to <outdir>/<pass>.
Run `ls` on the result in pass order: names keep gcc's numbers."""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib

src, out, fn = sys.argv[1:4]
flags = sys.argv[4:] or ['-fdump-tree-all-details', '-fdump-rtl-ce1-details', '-fdump-rtl-bbro-details']
os.makedirs(out, exist_ok=True)
text = open(src, newline='').read().replace('\r\n', '\n')
ok, o, d = irlib.compile_src(text, flags)
if not ok:
    print(o)
    sys.exit(1)
head = re.compile(r'^;; Function (\S+) ')
for name in os.listdir(d):
    if '.c.' not in name and not name.startswith('-.') and '.' not in name[1:]:
        continue
    p = os.path.join(d, name)
    if name == 'o.o' or os.path.isdir(p):
        continue
    keep = []
    on = False
    with open(p, errors='replace') as f:
        for l in f:
            m = head.match(l)
            if m:
                on = m.group(1) == fn
            if on:
                keep.append(l)
    if keep:
        m = re.search(r'\.(\d+[tri]\.[^.]+)$', name)
        tag = m.group(1) if m else name
        open(os.path.join(out, tag), 'w', newline='\n').writelines(keep)
irlib.cleanup(d)
print('wrote', out, len(os.listdir(out)), 'dumps')
