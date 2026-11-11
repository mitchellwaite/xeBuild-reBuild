"""oprvfreq.py po.dce : per bb in an RTL -blocks-details dump (oprvdump.sh): freq, source lines, LC labels, succs.
Cut one function out first, e.g. awk "/^;; Function parseOption/,/^;; Function parseCmdOptions/" dir/options.c.273r.rtl_dce"""
import re, sys
t = open(sys.argv[1]).read().split('\n')
cur = None
info = {}
order = []
mode = None
for l in t:
    m = re.match(r';; basic block (\d+), loop depth \d+, count \d+, freq (\d+)', l)
    if m:
        cur = int(m.group(1)); order.append(cur)
        info[cur] = {'freq': int(m.group(2)), 'lines': set(), 'lc': [], 'succ': []}
        mode = None
        continue
    if cur is None:
        continue
    if l.startswith(';;  pred:'):
        mode = 'pred'; continue
    m = re.match(r';;  succ:\s*(.*)', l)
    if m:
        mode = 'succ'
        if m.group(1).strip():
            info[cur]['succ'].append(m.group(1).strip())
        continue
    if mode == 'succ' and re.match(r';;\s{10,}\S', l):
        info[cur]['succ'].append(l[2:].strip()); continue
    if not l.startswith(';;'):
        mode = None
    for m in re.finditer(r'options\.c:(\d+)', l):
        info[cur]['lines'].add(int(m.group(1)))
    for m in re.finditer(r'"\*(LC\d+)"', l):
        if m.group(1) not in info[cur]['lc']:
            info[cur]['lc'].append(m.group(1))
seen = set()
for b in order:
    if b in seen:
        continue
    seen.add(b)
    i = info[b]
    ls = sorted(i['lines'])
    sc = '; '.join(re.sub(r'\s+', ' ', s) for s in i['succ'])
    print('%3d f=%-5d L%-16s %-12s -> %s' % (b, i['freq'], ','.join(map(str, ls[:4])), ' '.join(i['lc']), sc))
