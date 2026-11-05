"""Attempt 20: k3 of gen_ir248, E as a statement with a purpose: no-op on valid values through size's range (VRP2 knows [0x3000,0x3800], dom3 knows the mask), not an always-zero sum."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ir17lib import put, score
from gen_ir248 import forms, E

K3 = forms['k3']
ES = {
    # a mask from size that covers addr
    'or_fff': 'addr &= size | 0xfff;',
    'or_1fff': 'addr &= size | 0x1fff;',
    'or_7ff': 'addr &= size | 0x7ff;',
    'or_fffu': 'addr &= (unsigned)size | 0xfff;',
    'or_fff_l': '{ int mask = size | 0xfff; addr &= mask; }',
    'or_fff_ul': '{ unsigned mask = size | 0xfffu; addr &= mask; }',
    'dec_or': 'addr &= (size - 1) | 0xfff;',
    'dec_or_l': '{ int mask = (size - 1) | 0xfff; addr &= mask; }',
    'dec_or_7': 'addr &= (size - 1) | 0x7ff;',
    # clamps and tests against size
    'ge_1000': 'if (addr >= size) addr = 0x1000;',
    'gt_1000': 'if (addr > size) addr = 0x1000;',
    'min': 'addr = addr < size ? addr : size;',
    'min2': 'if (addr > size) addr = size;',
    'mod': 'addr %= size;',
    'umod': 'addr = (unsigned)addr % (unsigned)size;',
    'lt': 'if (size < 0x3000) addr = 0x1000;',
    'gt': 'if (size > 0x3800) addr = 0x1000;',
    'gt4': 'if (size > 0x4000) addr = 0x1000;',
    'le0': 'if (size <= 0) addr = 0x1000;',
    'not0': 'if (!size) addr = 0x1000;',
    'and4': 'if (size & ~0x3fff) addr = 0x1000;',
    'and7': 'if (size & 0x7ff) addr = 0x1000;',
    # size's own mask, as a test
    'maskne': 'if ((size & ~0x800u) != 0x3000) addr = 0x1000;',
    'maskne2': '{ unsigned base = size & ~0x800u; if (base != 0x3000) addr = 0x1000; }',
    # shifts and blocks
    'shr14': 'addr += size >> 14;',
    'and_shr14': 'addr &= ~(size >> 14);',
    'shl': 'addr <<= size >> 14;',
    'shr': 'addr >>= size >> 14;',
    'ud14': 'addr += (unsigned)size >> 14;',
    'neg': 'addr &= -(size > 0);',
    'mul': 'addr *= size > 0;',
    'div': 'addr /= size > 0;',
    # end of the image, back to the start
    'end': '{ int end = addr + size; addr = end - size; }',
    'endu': '{ unsigned end = addr + (unsigned)size; addr = end - size; }',
    'k3': E,
}
out = {k: K3.replace(E, v) for k, v in ES.items()}

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
