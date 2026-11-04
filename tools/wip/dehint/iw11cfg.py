"""python tools/wip/dehint/iw11cfg.py <dump file> [-a]: one line per basic block of a tree dump (dumps from iwdump.py):
index, freq if shown, PHIs of interest, last statement, successors.  Without -a statements other than the last are counted only."""
import re, sys

t = open(sys.argv[1], errors='replace').read()
full = '-a' in sys.argv
blocks = re.split(r'^\s*<bb (\d+)>:\s*$', t, flags=re.M)
for i in range(1, len(blocks), 2):
    n, body = blocks[i], blocks[i + 1]
    ls = [l.strip() for l in body.split('\n') if l.strip() and l.strip() != '}']
    phis = [l for l in ls if l.startswith('#') and 'PHI' in l]
    rest = [l for l in ls if not l.startswith('#')]
    succ = re.findall(r'goto <bb (\d+)>', body)
    nxt = blocks[i + 2] if i + 2 < len(blocks) else ''
    cond = [l for l in rest if l.startswith('if ')]
    last = cond[0] if cond else (rest[0] if rest and full else '')
    print('bb%-3s succ=%-10s phi=%d st=%d %s %s' % (n, ','.join(succ) or 'fall', len(phis), len(rest), last, (' | '.join(p[:90] for p in phis[:2]) if phis else '')))
    if full:
        for l in rest:
            print('      ', l[:100])
