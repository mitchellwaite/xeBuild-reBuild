"""Attempt 21, measurement only (nobody would write it): gen_ir226's unsplit S plus attempt 18's untested idea: `addr = 0x800` in the 3800 arm,
so the conversion isn't anticipated at S and PRE leaves it in E.  Does E's `mov ebx,edi` come, and what happens to the 3000 arm?
python gen_ir258.py [name] : sweep, or the loose diff of one form."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_ir226 import forms as F226, L38
from ir17lib import put, score, diff

forms = {}
for k, t in F226.items():
    if '.plain.' in k:
        continue
    forms[k + '.base'] = t
    forms[k + '.kill'] = t.replace(L38, 'addr = 0x800; ' + L38, 1)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(diff(put(forms[sys.argv[1]])))
        sys.exit()
    res = []
    for k, t in forms.items():
        s = score(put(t))
        if s[0] != 'E':
            res.append((s[1], s[0], k))
    res.sort()
    for r in res[:10]:
        print(r)
    b = res[0][2]
    print(b)
    print(diff(put(forms[b])))
    bk = next(r[2] for r in res if r[2].endswith('.kill'))
    print(bk)
    print(diff(put(forms[bk])))
