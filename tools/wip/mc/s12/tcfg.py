"""tree CFG summary of mode_client (last copy) in a profile_estimate dump: python tcfg.py DUMP [lo hi]"""
import re, sys
t = open(sys.argv[1]).read()
i = t.rindex(';; Function mode_client'); t = t[i:]; j = t.find('\n;; Function ', 10); t = t[:j if j > 0 else None]
lo, hi = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, 999)
for m in re.finditer(r';;   basic block (\d+),.*?\n(.*?)(?=;;   basic block|\Z)', t, re.S):
    b = int(m.group(1))
    if not lo <= b <= hi: continue
    body = m.group(2)
    succ = re.findall(r';;\s+(?:succ:)?\s+(\d+) \[([\d.]+)%\]', body.split(';;    succ:')[-1]) if ';;    succ:' in body else []
    calls = re.findall(r'(\w+) \(', '\n'.join(l for l in body.split('\n') if not l.startswith(';;')))
    stmt = [l.strip() for l in body.split('\n') if l.strip() and not l.startswith(';;')][:2]
    print(b, '->', ' '.join('%s[%s]' % s for s in succ), '|', ' '.join(calls)[:60], '|', ' / '.join(stmt)[:70])
