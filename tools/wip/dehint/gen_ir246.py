"""Attempt 19: no attribute.  At ce3, S_bad's fall-through decides: if it is the arm's edge block and that block falls through into the 3000 arm, IF-CASE-1 refuses it and IF-CASE-2 refuses E's (less likely) block.
S_bad merges with the bad log's block, so the bad log must be written right before the 3000 arm."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ir17lib import put, score, diff, LOG0, L38, L30, NOTSANE, HEAD, LIM

EX = {
    'c9': '{ int excess = ((unsigned)size & ~0x800u) - 0x3000; addr += excess; }',
    'c7': 'addr += (int)(((unsigned)size & ~0x800u) ^ 0x3000u);',
}
TOP = f'''void getImageSmc(void)
{{
{HEAD} int ok = addr != 0;
 unsigned t, lim;
 int wrong, bad, o, out;
 if (ok <= 0) {{ {LOG0} addr = 0x1000; }}
 t = addr;
 if (t != 0x1000) {{ wrong = t != 0x800; if (wrong > 0) goto badAddr; }}
fixSize:
 bad = size != 0x3000 && size != 0x3800;
'''
CHECK = f'''lim = {LIM};
 if ((unsigned)addr != lim) {{ out = (unsigned)addr >= lim; if (out <= 0) {{ loadSmc(addr, size); return; }} }}
 {NOTSANE} return;
'''
BADL = f'badAddr: {LOG0} addr = 0x1000; goto fixSize;\n'
SIZEF = {
    # o's test jumps to the 3000 arm, written after the bad log
    'g1': lambda e: f'''if (bad > 0) {{ o = addr != 0x800; if (o > 0) goto use3000; {L38} }} else {{ {e} }}
 goto check;
{BADL} use3000: {L30} check: {CHECK}}}''',
    'g2': lambda e: f'''if (bad > 0) {{ o = addr != 0x800; if (o <= 0) {{ {L38} goto check; }} goto use3000; }}
 {e} goto check;
{BADL} use3000: {L30} check: {CHECK}}}''',
    'g3': lambda e: f'''if (bad <= 0) {{ {e} goto check; }}
 o = addr != 0x800; if (o > 0) goto use3000; {L38} goto check;
{BADL} use3000: {L30} check: {CHECK}}}''',
    'g4': lambda e: f'''if (bad > 0) {{ o = addr != 0x800; if (o <= 0) {{ {L38} }} else goto use3000; }} else {{ {e} }}
 goto check;
{BADL} use3000: {L30} check: {CHECK}}}''',
    # E late as well
    'g5': lambda e: f'''if (bad > 0) {{ o = addr != 0x800; if (o > 0) goto use3000; {L38} goto check; }} else goto sizeOk;
{BADL} use3000: {L30} goto check; sizeOk: {e} check: {CHECK}}}''',
    # check in the middle, 3000 after (string order wrong, for comparison)
    'g6': lambda e: f'''if (bad > 0) {{ o = addr != 0x800; if (o > 0) goto use3000; {L38} }} else {{ {e} }}
 check: {CHECK}
{BADL} use3000: {L30} goto check; }}''',
}
forms = {f'{g}.{ek}': TOP + f(e) for (g, f), (ek, e) in itertools.product(SIZEF.items(), EX.items())}

if __name__ == '__main__':
    res = []
    for k, f in forms.items():
        s = score(put(f))
        if s[0] == 'E':
            print(k, s[1][:300])
            continue
        res.append((s[1], s[0], k, s[2], s[3]))
    res.sort(key=lambda x: (x[0], x[1]))
    for r in res:
        print(r)
