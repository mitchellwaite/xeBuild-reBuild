"""Attempt 20: E as a recheck of size with a purpose: a size other than the good ones gets addr a value that the bound check below rejects.  The value must be non-constant at PRE (a constant gives PRE its leader, v_tern, maskne)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ir17lib import put, score
from gen_ir252 import SRC, OLD_E

M = '(size & ~0x800u)'
LIMX = '528 * xb.dumpPages'
ES = {
    # force the bound check to fail
    'lim_b': f'{{ unsigned base = {M}; if (base != 0x3000) addr = {LIMX}; }}',
    'lim': f'if ({M} != 0x3000) addr = {LIMX};',
    'lim_v': f'{{ int valid = {M} == 0x3000; if (!valid) addr = {LIMX}; }}',
    'lim_tern': f'addr = {M} == 0x3000 ? addr : {LIMX};',
    'pages': f'{{ unsigned base = {M}; if (base != 0x3000) addr = xb.dumpPages; }}',
    # size is what is out of range; address past what?
    'addsz': f'{{ unsigned base = {M}; if (base != 0x3000) addr += size; }}',
    'addbase': f'{{ unsigned base = {M}; if (base != 0x3000) addr += base; }}',
    'sz': f'{{ unsigned base = {M}; if (base != 0x3000) addr = size; }}',
    'sz0': f'if ({M} != 0x3000) addr = size;',
    'sz_v': f'{{ int valid = {M} == 0x3000; if (!valid) addr = size; }}',
    'sz_rv': f'{{ unsigned base = {M}; if (base == 0x3000) goto check; addr = size; }}',
    'neg': f'{{ unsigned base = {M}; if (base != 0x3000) addr = -size; }}',
    'not': f'{{ unsigned base = {M}; if (base != 0x3000) addr = ~addr; }}',
    'negad': f'{{ unsigned base = {M}; if (base != 0x3000) addr = -addr; }}',
    'shift': f'{{ unsigned base = {M}; if (base != 0x3000) addr <<= 1; }}',
    # masks
    'al1': f'{{ unsigned base = {M}; int m = base & 0xfff; addr &= ~m; }}',
    'al2': f'{{ unsigned base = {M}; int m = base % 0x1000; addr &= ~m; }}',
    'al3': f'{{ unsigned base = {M}; int m = base % 0x1000; addr -= addr & m; }}',
    'al4': f'{{ unsigned base = {M}; int m = base & 0xfff; addr -= addr & m; }}',
    'al5': f'{{ unsigned base = {M}; int m = base & 0x7ff; addr &= ~m; }}',
    'al6': f'{{ unsigned base = {M}; addr &= ~(int)(base & 0xfff); }}',
    'al7': f'{{ int m = {M} & 0xfff; addr &= ~m; }}',
    'al8': f'{{ int m = size & 0x7ff; addr &= ~m; }}',
    'al9': f'{{ unsigned m = (unsigned)size & 0x7ff; addr &= ~m; }}',
    'al10': f'{{ int m = size % 0x800; addr &= ~m; }}',
}
out = {k: SRC.replace(OLD_E, '\t' + v + '\n') for k, v in ES.items()}

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
