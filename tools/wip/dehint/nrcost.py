"""python tools/wip/dehint/nrcost.py <src.c> ...: for the clone, each pseudo in the callee-saved group: final MEM and GENERAL_REGS cost, avail regs, disposition; got's margin against the caller-save threshold."""
import os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
for src in sys.argv[1:]:
    d = os.path.join(ROOT, 'build', 'nr', 'cost', os.path.basename(os.path.dirname(src)) + '_' + os.path.basename(src)[:-2])
    o = subprocess.run([sys.executable, os.path.join(ROOT, 'tools/wip/dehint/nrdump.py'), d, src], capture_output=True, text=True).stdout
    t = open(os.path.join(d, 'a.c.255r.ira')).read()
    i = t.index(';; Function netRecvVerbose.constprop'); j = t.find('\n;; Function', i + 10); s = t[i:j]
    print('==', src)
    last = {}
    for m in re.finditer(r'a(\d+)\(r(\d+),l0\) costs:(.*?)MEM:(-?\d+),(-?\d+)', s):
        g = re.search(r'GENERAL_REGS:(-?\d+),(-?\d+)', m.group(3))
        last[m.group(2)] = (m.group(5), g.group(2) if g else '?')
    sec = o.split('== IRA netRecvVerbose\n')[0]
    for l in sec.split('\n'):
        m = re.match(r'r(\d+)\s+(\S+)\s+mem=\S+\s+(.*)', l)
        if m and m.group(1) in last and int(last[m.group(1)][0]) > 300:
            print('  r%s %-10s MEM %s class %s -> %s' % (m.group(1), m.group(2), last[m.group(1)][0], last[m.group(1)][1], m.group(3)))
    for m in re.finditer(r'Pushing a(\d+)\(r(\d+),l0\)', s):
        pass
    print('  avail:', ' '.join(sorted(set(re.findall(r'a\d+r\d+ of \S+ has \d+ avail', s)))[:0]))
    for l in s.split('\n'):
        if 'Spilling' in l or 'Pushing' in l and 'got' in l:
            print('  ', l.strip()[:100])
