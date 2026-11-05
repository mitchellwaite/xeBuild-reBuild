"""Attempt 19: E statements as gen_ir241, with size's mask in unsigned (so it's the range test's own value, a PHI at E that dom3 folds to the constant) and the sum on int addr (no separate conversion of addr for PRE to take)."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_ir241 import body, text, score, att, subsets

M = '((unsigned)size & ~0x800u)'
ELS = {
    'c1': f'addr += (int)({M} - 0x3000u);',
    'c2': f'addr += (int){M} - 0x3000;',
    'c3': f'addr = addr + (int)({M} - 0x3000);',
    'c4': f'addr -= (int)(0x3000u - {M});',
    'c5': f'addr ^= (int)({M} - 0x3000u);',
    'c6': f'addr |= (int)({M} ^ 0x3000u);',
    'c7': f'addr += (int)({M} ^ 0x3000u);',
    'c8': f'addr -= 0x3000 - (int){M};',
    'c9': f'{{ int d = {M} - 0x3000; addr += d; }}',
    'c10': f'{{ unsigned m = {M}; addr += (int)(m - 0x3000); }}',
    'c11': f'{{ unsigned m = {M}; if (m != 0x3000) addr = 0; }}',
    'c12': f'if ({M} != 0x3000u) addr = 0x1000;',
    'c13': f'if ({M} != 0x3000u) addr = 0;',
}
forms = {}
for (ek, e), sub in itertools.product(ELS.items(), subsets):
    forms['.'.join((ek, ''.join(x[3] + x[-1] for x in sub) or 'a0'))] = body(att(sub), e)

if __name__ == '__main__':
    res = []
    for k, f in forms.items():
        s = score(text(f))
        if s[0] == 'E':
            print(k, s[1][:200])
            continue
        res.append((s[1], s[0], k, s[2]))
    res.sort(key=lambda x: (x[0], x[1]))
    print(len(res))
    for r in res[:30]:
        print(r)
    for e in ELS:
        print(e, [r[:3] for r in res if r[2].startswith(e + '.')][:3])
