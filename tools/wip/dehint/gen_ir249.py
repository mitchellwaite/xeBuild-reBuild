"""Attempt 19: k3 of gen_ir248 (no pin, no attribute), the E statement's spellings, and whether the plain-C predictor flags are still needed."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ir17lib import put, score
from gen_ir248 import forms, E

K3 = forms['k3']
ES = {
    'c9': E,
    'nocast': '{ int excess = (size & ~0x800u) - 0x3000; addr += excess; }',
    'nodecl': 'addr += (int)((size & ~0x800u) - 0x3000);',
    'ne': 'addr += (size & ~0x800u) != 0x3000;',
    'xor': 'addr ^= (int)((size & ~0x800u) ^ 0x3000);',
    'or': 'addr |= (int)((size & ~0x800u) ^ 0x3000);',
    'sub3': '{ int excess = (size & ~0x800u) - 0x3000; addr -= excess; }',
    'ux': '{ unsigned rest = size & ~0x800u; int excess = rest - 0x3000; addr += excess; }',
    'ic': '{ int rest = size & ~0x800u; addr += rest - 0x3000; }',
    'empty': ';',
}
out = {k: K3.replace(E, v) for k, v in ES.items()}
# hints in plain C that may have only been needed by the old shape
FL = {
    'ok': ('int ok = addr != 0;', 'int ok = addr != 0;', 'if (ok <= 0)', 'if (!addr)'),
    'wrong': ('wrong = t != 0x800; if (wrong > 0) goto badAddr;', 'if (t != 0x800) goto badAddr;'),
    'bad': ('if (bad > 0) {', 'if (bad) {'),
    'o': ('o = addr != 0x800; if (o > 0) goto use3000;', 'if (addr != 0x800) goto use3000;'),
    't': ('if (t != 0x1000) {', 'if (addr != 0x1000) {'),
}
for k, r in FL.items():
    x = K3
    for a, b in zip(r[0::2], r[1::2]):
        assert a in x, a
        x = x.replace(a, b)
    out['fl_' + k] = x

if __name__ == '__main__':
    res = []
    for k, f in out.items():
        s = score(put(f))
        if s[0] == 'E':
            print(k, s[1][:300])
            continue
        res.append((s[1], s[0], k, s[2], s[3]))
    res.sort(key=lambda x: (x[0], x[1]))
    for r in res:
        print(r)
