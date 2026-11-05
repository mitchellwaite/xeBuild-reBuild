"""Attempt 20: only the unsigned mask is known to dom3 and not to vrp1 (`size` itself is int, (int)_20 is defined above the tests, so ranges never reach it; `(unsigned)size` has its range at vrp1 already).
So: base = size & ~0x800u (0x3000 after dom3) and a statement on addr that VRP2 folds once base is a constant: clamps, masks, modulo."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ir17lib import put, score
from gen_ir248 import forms, E

K3 = forms['k3']
DECL = {
    'i': 'int base = size & ~0x800u;',
    'u': 'unsigned base = size & ~0x800u;',
}
ST = {
    'min_if': 'if (addr > base) addr = base;',
    'min_ifc': 'if (addr > (int)base) addr = base;',
    'min_ifge': 'if (addr >= base) addr = base;',
    'min_tern': 'addr = addr < (int)base ? addr : (int)base;',
    'min_ternu': 'addr = (unsigned)addr < (unsigned)base ? addr : (int)base;',
    'min_ifu': 'if ((unsigned)addr > (unsigned)base) addr = base;',
    'ge1000': 'if (addr >= (int)base) addr = 0x1000;',
    'ge1000u': 'if ((unsigned)addr >= (unsigned)base) addr = 0x1000;',
    'gt1000': 'if (addr > (int)base) addr = 0x1000;',
    'mod': 'addr %= (int)base;',
    'modu': 'addr = (unsigned)addr % (unsigned)base;',
    'and1': 'addr &= base | 0xfff;',
    'and1i': 'addr &= (int)(base | 0xfff);',
    'and2': 'addr &= 2 * base - 1;',
    'and2i': 'addr &= (int)(2 * base - 1);',
    'and3': 'addr &= base + 0xfff;',
    'and3i': 'addr &= (int)(base + 0xfff);',
    'sh': 'addr += base >> 14;',
    'shi': 'addr += (int)(base >> 14);',
    'and4': 'addr &= ~(base >> 14);',
    'and4i': 'addr &= (int)~(base >> 14);',
    'sum': 'addr += base - 0x3000;',
    'sumi': 'addr += (int)(base - 0x3000);',
}
out = {}
for (dk, d), (sk, s) in itertools.product(DECL.items(), ST.items()):
    out[f'{dk}.{sk}'] = K3.replace(E, '{ ' + d + ' ' + s + ' }')

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
