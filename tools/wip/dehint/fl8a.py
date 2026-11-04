"""fl8a.py: parseIni's local types.
  python fl8a.py single      one var, one type, at every subset of T1-T3
  python fl8a.py rand N      random combinations of types that moved something, from fl8a_single's log
"""
import os, random, sys
import fl8lib as T

TY = ['int', 'unsigned', 'uint32_t', 'long', 'unsigned_long', 'size_t', 'BOOL', 'short', 'long_long']
ALT = {v: TY for v in T.VARS}
ALT['noCrc'] = ['int', 'unsigned', 'long', 'BOOL', 'char', 'unsigned_char', 'size_t']
ALT['crc'] = ['int', 'unsigned', 'long', 'unsigned_long', 'size_t', 'BOOL']


def single():
    V = {}
    for d in T.SUBS:
        V[d + '|'] = T.state(d + '|')
        for v, tys in ALT.items():
            for t in tys:
                if t == T.DEF[v]:
                    continue
                lb = '%s|t.%s=%s' % (d, v, t)
                V[lb] = T.state(lb)
        for v in ('tmp', 'label'):
            lb = '%s|t.%s=unsigned_char' % (d, v)
            V[lb] = T.state(lb)
    rs = T.run(V, 'single')
    T.floors(rs)
    base = {r[3]: r[0] for r in rs if r[3].endswith('|')}
    moved = {}
    for r in rs:
        d, _, a = r[3].partition('|')
        if not a:
            continue
        x = moved.setdefault(a, {})
        x[d] = r[0] - base[d + '|']
    print('per edit: min, max change, score at none-dropped, all-dropped')
    sc = {r[3]: r[0] for r in rs}
    for a, x in sorted(moved.items(), key=lambda kv: min(kv[1].values())):
        print(a, min(x.values()), max(x.values()), sc['|' + a], sc['T1,T2,T3|' + a], sc['T1,T3|' + a])


if __name__ == '__main__':
    single()
