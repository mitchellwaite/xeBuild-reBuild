"""python tools/wip/dehint/nrobjbest.py <gen name> [max V+C]: nrsweep can't see alignment or .rdata, so run nrobj on sweep rows.
Reads build/nr/<gen>.txt (nrdef output with NR_TAGS=1 NR_TOP=1000) and prints text/data counts per row with V+C at most N (default 0)."""
import os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
gen = sys.argv[1]
mx = int(sys.argv[2]) if len(sys.argv) > 2 else 0
files = []
for l in open(os.path.join(ROOT, 'build', 'nr', gen + '.txt')):
    m = re.match(r'V=(\d+) C=(\d+) ', l)
    if not m or int(m.group(1)) + int(m.group(2)) > mx:
        continue
    for tag, v in re.findall(r'(\S+) (v\d+\.c)', l.partition(' e.g. ')[2]):
        files.append((tag, os.path.join(ROOT, 'build', 'nr', gen, v)))
tags = {os.path.basename(p): t for t, p in files}
for i in range(0, len(files), 8):
    o = subprocess.run([sys.executable, os.path.join(ROOT, 'tools/wip/dehint/nrobj.py')] + [p for _, p in files[i:i + 8]], capture_output=True, text=True).stdout
    for l in o.split('\n'):
        m = re.match(r'(v\d+\.c) (text \d+ data \d+)', l)
        if m:
            print(m.group(2), tags[m.group(1)], m.group(1))
