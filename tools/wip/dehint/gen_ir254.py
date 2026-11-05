"""Attempt 21: getImageSmc from scratch, no flags at all, starting from getImageKv's form.
Axes: Z (zero and bad-address fix, including one shared fallback assignment), S (size fix), C (sane test), T (types).
python gen_ir254.py [name] : sweep, or print the loose diff of one form."""
import itertools, multiprocessing, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ir17lib import put, score, diff, LOG0, L38, L30, NOTSANE, LIM

GOOD = 'addr != 0x800 && addr != 0x1000'
Z = {
    'kv': f'if (!addr) {{ {LOG0} addr = 0x1000; }} if ({GOOD}) {{ {LOG0} addr = 0x1000; }}',
    'kvr': f'if (!addr) {{ {LOG0} addr = 0x1000; }} if (addr != 0x1000 && addr != 0x800) {{ {LOG0} addr = 0x1000; }}',
    'else': f'if (!addr) {{ {LOG0} addr = 0x1000; }} else if ({GOOD}) {{ {LOG0} addr = 0x1000; }}',
    'share': f'if (!addr) {{ {LOG0} }} else if ({GOOD}) {{ {LOG0} }} else goto addrOk; addr = 0x1000; addrOk:',
    'fb': f'if (!addr) {{ {LOG0} goto fb; }} if ({GOOD}) {{ {LOG0} fb: addr = 0x1000; }}',
    'or': f'if (!addr || ({GOOD})) {{ {LOG0} addr = 0x1000; }}',
    'nest': f'if (!addr) {{ {LOG0} addr = 0x1000; }} if (addr != 0x1000) {{ if (addr != 0x800) {{ {LOG0} addr = 0x1000; }} }}',
    'nestu': f'if (!addr) {{ {LOG0} addr = 0x1000; }} {{ unsigned t = addr; if (t != 0x1000) {{ if (t != 0x800) {{ {LOG0} addr = 0x1000; }} }} }}',
}
ARM38 = lambda: L38
S = {
    'and': f'if (size != 0x3000 && size != 0x3800) {{ if (addr == 0x800) {{ {L38} }} else {{ {L30} }} }}',
    'and30': f'if (size != 0x3000 && size != 0x3800) {{ if (addr != 0x800) {{ {L30} }} else {{ {L38} }} }}',
    'orelse': f'if (size == 0x3000 || size == 0x3800) ; else if (addr == 0x800) {{ {L38} }} else {{ {L30} }}',
    'sw': f'switch (size) {{ case 0x3000: case 0x3800: break; default: if (addr == 0x800) {{ {L38} }} else {{ {L30} }} }}',
}
C = {
    'lt': f'if (addr < {LIM}) loadSmc(addr, size); else {NOTSANE}',
    'ge': f'if (addr >= {LIM}) {NOTSANE} else loadSmc(addr, size);',
    'gr': f'if (addr >= {LIM}) {{ {NOTSANE} return; }} loadSmc(addr, size);',
    'lr': f'if (addr < {LIM}) {{ loadSmc(addr, size); return; }} {NOTSANE}',
}
T = {'ii': ('int', 'int'), 'ui': ('uint32_t', 'int'), 'iu': ('int', 'uint32_t'), 'uu': ('uint32_t', 'uint32_t')}


def text(z, s, c, t):
    a, b = T[t]
    return f'''void getImageSmc(void)
{{
 struct flashhdr *h = (struct flashhdr *)xb.dump;
 {a} addr = SWAP32(h->smcBootAddr);
 {b} size = SWAP32(h->smcBootSize);
 {Z[z]}
 {S[s]}
 {C[c]}
}}'''


def one(k):
    r = score(put(text(*k)))
    return ('.'.join(k), r)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(diff(put(text(*sys.argv[1].split('.')))))
        sys.exit()
    keys = list(itertools.product(Z, S, C, T))
    with multiprocessing.Pool(4) as p:
        res = p.map(one, keys, 8)
    res = [x for x in res if x[1][0] != 'E']
    res.sort(key=lambda x: (x[1][1], x[1][0]))
    for k, r in res[:30]:
        print(k, r[0], r[1], list(r[2]), r[3])
    print(len(res), 'of', len(keys))
