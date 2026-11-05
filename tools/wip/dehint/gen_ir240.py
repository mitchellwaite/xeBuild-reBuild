"""Attempt 19: loops that survive vrp1 and dom2 and go at cunroll: address and size checks over small tables or retried.
parts: Z (zero test), A (address check), S (size check), E (else arm statement), attr.  No pin in any form."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ir17lib import put, score, diff, LOG0, L38, L30, NOTSANE, HEAD, LIM

ATT = {'a0': '', 'i2': '__attribute__((optimize("no-if-conversion2"))) ',
       'a3': '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) '}

Z = {
    'z': f'ok = addr != 0; if (ok <= 0) {{ {LOG0} addr = 0x1000; }}',
    'zp': f'if (!addr) {{ {LOG0} addr = 0x1000; }}',
}
A = {
    # plain, the current
    'pl': f'''t = addr; if (t != 0x1000) {{ wrong = t != 0x800; if (wrong > 0) {{ {LOG0} addr = 0x1000; }} }}''',
    # table scan, break
    'tb': f'''for (i = 0; i < 2; i++) if (addr == goodAddr[i]) break;
 if (i == 2) {{ {LOG0} addr = 0x1000; }}''',
    'tf': f'''found = 0; for (i = 0; i < 2; i++) if (addr == goodAddr[i]) found = 1;
 if (!found) {{ {LOG0} addr = 0x1000; }}''',
    'tf2': f'''found = 0; for (i = 0; i < 2 && !found; i++) if (addr == goodAddr[i]) found = 1;
 if (!found) {{ {LOG0} addr = 0x1000; }}''',
    # retry
    'rw': f'''while (addr != 0x1000 && addr != 0x800) {{ {LOG0} addr = 0x1000; }}''',
    'rd': f'''do {{ retry = 0; if (addr != 0x1000 && addr != 0x800) {{ {LOG0} addr = 0x1000; retry = 1; }} }} while (retry);''',
}
SZ = {
    'pl': lambda arms, els: f'''bad = size != 0x3000 && size != 0x3800; if (bad > 0) {{ {arms} }} else {{ {els} }}''',
    'tb': lambda arms, els: f'''for (i = 0; i < 2; i++) if (size == goodSize[i]) break;
 if (i == 2) {{ {arms} }} else {{ {els} }}''',
    'tf': lambda arms, els: f'''found = 0; for (i = 0; i < 2; i++) if (size == goodSize[i]) found = 1;
 if (!found) {{ {arms} }} else {{ {els} }}''',
    'tf2': lambda arms, els: f'''found = 0; for (i = 0; i < 2 && !found; i++) if (size == goodSize[i]) found = 1;
 if (!found) {{ {arms} }} else {{ {els} }}''',
    'rw': lambda arms, els: f'''while (size != 0x3000 && size != 0x3800) {{ {arms} }} {els}''',
    'rd': lambda arms, els: f'''do {{ retry = 0; if (size != 0x3000 && size != 0x3800) {{ {arms} retry = 1; }} }} while (retry); {els}''',
}
ARMS = {
    'p': f'o = addr != 0x800; if (o <= 0) {{ {L38} }} else {{ {L30} }}',
    'k': f'o = addr != 0x800; if (o <= 0) {{ {L38} addr = 0x800; }} else {{ {L30} }}',
}
END = {
    'n': f'''lim = {LIM}; if ((unsigned)addr != lim) {{ out = (unsigned)addr >= lim; if (out <= 0) {{ loadSmc(addr, size); return; }} }} {NOTSANE}''',
    'l': f'''lim = {LIM}; if ((unsigned)addr < lim) {{ loadSmc(addr, size); return; }} {NOTSANE}''',
}
DECL = '''static const int goodAddr[2] = { 0x1000, 0x800 };
static const int goodSize[2] = { 0x3000, 0x3800 };
'''


def fn(att, z, a, s, arms, end, els=';'):
    return f'''{DECL}{ATT[att]}void getImageSmc(void)
{{
{HEAD}
 int ok, i, found, retry, wrong, bad, o, out;
 unsigned t, lim;
 {Z[z]}
 {A[a]}
 {SZ[s](ARMS[arms], els)}
 {END[end]}
}}'''


if __name__ == '__main__':
    res = []
    for att, z, a, s, arms, end in itertools.product(ATT, Z, A, SZ, ARMS, END):
        k = '.'.join((att, z, a, s, arms, end))
        r = score(put(fn(att, z, a, s, arms, end)))
        if r[0] == 'E':
            print(k, r[1][:300])
            continue
        res.append((r[1], r[0], k, sum(r[2].values())))
    res.sort()
    print(len(res))
    for r in res[:40]:
        print(r)
    for at in ATT:
        print(at, [r for r in res if r[2].startswith(at)][:6])
    for s in SZ:
        print('size', s, [r for r in res if r[2].split('.')[3] == s][:3])
    for s in A:
        print('addr', s, [r for r in res if r[2].split('.')[2] == s][:3])
