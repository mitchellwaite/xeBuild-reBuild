"""opdz.py: trims of applyIniOptions' dz1/dz2 dummy blocks on src/options.c (pins, the dzc
indirection), scored with optlib, singly and combined."""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

D1 = '	if (0) { dzc1: ; goto dz1; dz1: __asm__ volatile ("" :: "i"(1));  __builtin_unreachable(); }\n'
D2 = '	if (0) { dzc2: ; goto dz2; dz2: __asm__ volatile ("" :: "i"(4));  __builtin_unreachable(); }\n'
E = {
    'pin1': [(D1, D1.replace('__asm__ volatile ("" :: "i"(1));  ', ''))],
    'pin2': [(D2, D2.replace('__asm__ volatile ("" :: "i"(4));  ', ''))],
    'pin1e': [(D1, D1.replace('__asm__ volatile ("" :: "i"(1));', '__asm__ volatile ("");'))],
    'pin2e': [(D2, D2.replace('__asm__ volatile ("" :: "i"(4));', '__asm__ volatile ("");'))],
    'ind1': [(D1, D1.replace('dzc1: ; goto dz1; dz1:', 'dz1:')), (':::: dzc1)', ':::: dz1)')],
    'ind2': [(D2, D2.replace('dzc2: ; goto dz2; dz2:', 'dz2:')), (':::: dzc2)', ':::: dz2)')],
}


def apply(t, names):
    for n in names:
        for a, b in E[n]:
            if a not in t:
                return None
            t = t.replace(a, b)
    return t


if __name__ == '__main__':
    base = optlib.read_src(optlib.SRC)
    combos = [c for k in (1, 2) for c in itertools.combinations(E, k)
              if not ({'pin1', 'pin1e'} <= set(c) or {'pin2', 'pin2e'} <= set(c))]

    def one(c):
        t = c and apply(base, c)
        return c, optlib.score_text(t) if t else {'compile': 'n/a'}
    with ThreadPoolExecutor(6) as p:
        for c, r in p.map(one, combos):
            print('%-14s %s' % ('+'.join(c), optlib.fmt(r)), flush=True)
