"""python tools/wip/dehint/bdsubset.py [fn..]: every subset of a function's tricks off together; per subset size, the best three.
Strict lines for that function; BDLOOSE=1 for loose.  BDBASE as in bdtricks."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, bdtricks

CRC = 'crc5,crc7,crc8,crc9,crc10,crc12,crc13'
G = {
    'extract': ['exp_200', 'pin_i', 'exp_210', 'exp_400', 'pin_src', 'lab_nf1', 'lab_nf2'],
    'patchsmc': ['nei_smc', 'cb1', 'cb2', 'cb3', 'cb4'],
    'checkbl': ['nei_chk', 'pin_type', 'lab_size', 'cb5', 'pin_m', CRC],
    'loadbl': ['exp_t10', 'lab_t5le', 'exp_pr', 'lab_badsize', 'exp_27', 'pin_d', 'vol_fail'],
    'crc': ['exp_verbose', 'pin_e'],
    'console': ['exp_t9', 'lab_none'],
}
names = sys.argv[1:] or list(G)
b = bdtricks.base()
for g in names:
    it = G[g]
    sets = [c for k in range(1, len(it) + 1) for c in itertools.combinations(it, k)]

    def one(c):
        off = [x for s in c for x in s.split(',')]
        return c, bdtricks.score(off, b)
    with bdtricks.pool() as p:
        rs = list(p.map(one, sets))
    print('==', g)
    for k in range(1, len(it) + 1):
        r = sorted((x for x in rs if len(x[0]) == k), key=lambda x: x[1].get('total', 10**9))
        for c, v in r[:3]:
            print('  %d %5s %s | %s' % (k, v.get('total'), '+'.join(s.split(',')[0] for s in c), ','.join('%s:%d' % (n[1:], m) for n, m in v.get('per', {}).items())[:80]))
