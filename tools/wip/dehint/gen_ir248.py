"""Attempt 19: h1 of gen_ir247 with something after the not-sane block: the return block's previous block has no early return prediction; g6/h3 have another block there.  E is a block with no strings, so it goes last."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ir17lib import put, score, diff, LOG0, L38, L30, NOTSANE, LIM
from gen_ir246 import TOP, BADL, EX
ARMS = f'if (bad > 0) {{ o = addr != 0x800; if (o > 0) goto use3000; {L38} }} else goto sizeOk;'
CHK = f'''check: lim = {LIM};
 if ((unsigned)addr != lim) {{ out = (unsigned)addr >= lim; if (out <= 0) goto load; }}
 goto notSane;'''
CHK2 = f'''check: lim = {LIM};
 if ((unsigned)addr != lim) {{ out = (unsigned)addr >= lim; if (out <= 0) {{ loadSmc(addr, size); return; }} }}
 {NOTSANE} return;'''
E = EX['c9']
forms = {
 'k1': TOP + f'''{ARMS}
 {CHK}
{BADL} use3000: {L30} goto check;
 load: loadSmc(addr, size); return;
 notSane: {NOTSANE} return;
 sizeOk: {E} goto check; }}''',
 'k2': TOP + f'''{ARMS}
 goto check;
{BADL} use3000: {L30}
 {CHK2}
 sizeOk: {E} goto check; }}''',
 'k3': TOP + f'''if (bad > 0) {{ o = addr != 0x800; if (o > 0) goto use3000; {L38} goto check; }} goto sizeOk;
{BADL} use3000: {L30}
 {CHK2}
 sizeOk: {E} goto check; }}''',
 'k4': TOP + f'''if (bad > 0) {{ o = addr != 0x800; if (o > 0) goto use3000; {L38} goto check; }} else {{ {E} goto check; }}
{BADL} use3000: {L30}
 {CHK2}
 }}''',
 'k5': TOP + f'''{ARMS}
 goto check;
{BADL} use3000: {L30}
 {CHK.replace('goto notSane;','goto notSane;')}
 load: loadSmc(addr, size); return;
 notSane: {NOTSANE} return;
 sizeOk: {E} goto check; }}''',
 'k6': TOP + f'''{ARMS}
 goto check;
{BADL} use3000: {L30}
 {CHK}
 notSane: {NOTSANE} return;
 load: loadSmc(addr, size); return;
 sizeOk: {E} goto check; }}''',
}
if __name__ == '__main__':
    res = []
    for k, f in forms.items():
        s = score(put(f))
        if s[0] == 'E':
            print(k, s[1][:300]); continue
        res.append((s[1], s[0], k, s[2], s[3]))
    res.sort(key=lambda x: (x[0], x[1]))
    for r in res: print(r)
