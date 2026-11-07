"""python tools/wip/dehint/bdpred.py fn.profile_estimate: each conditional bb's test, with the
predictors gcc 6 printed for it ("Predictions for bb N") and the combined probability
(of the true edge, as profile_estimate prints it: the first predicted edge)."""
import re, sys

t = open(sys.argv[1]).read()
preds = {}
cur = None
for l in t.splitlines():
    m = re.match(r'Predictions for bb (\d+)', l)
    if m:
        cur = int(m.group(1)); preds[cur] = []; continue
    if cur is not None:
        m = re.match(r'\s+(.*) heuristics(?: \(ignored\))?: ([\d.]+)%', l)
        if m:
            preds[cur].append((m.group(1), m.group(2))); continue
        cur = None
# body: the copy with statements (';;   basic block N' headers)
bbs = {}
cur = None
for l in t.splitlines():
    m = re.match(r';;   basic block (\d+),', l)
    if m:
        cur = int(m.group(1)); bbs[cur] = []; continue
    if cur is not None:
        if not l.startswith(';;'):
            bbs[cur].append(l.strip())
for b in sorted(preds):
    lines = bbs.get(b, [])
    cond = [l for l in lines if l.startswith('if (') or l.startswith('switch')]
    calls = [re.sub(r'\s+', ' ', l) for l in lines if re.search(r'\b\w+ \(', l) and not l.startswith('if') and not l.startswith('#') and not l.startswith(';;')]
    p = ', '.join('%s %s' % (n.replace('(on trees) ', '').replace(' heuristics', ''), v) for n, v in preds[b] if n not in ('first match',))
    print('bb %-4d %-40s | %s' % (b, (cond[0] if cond else '?')[:40], p))
    for c in calls[-2:]:
        print('         %s' % c[:110])
