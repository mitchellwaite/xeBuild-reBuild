"""Attempt 19: g6 of gen_ir246 has the reference's code with no attribute, only the 3000 string in the wrong place (.rdata): the arm is written after the check.
So keep the check's compare there and write the strings' blocks (load, not sane) after the 3000 arm."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ir17lib import put, score, diff, LOG0, L38, L30, NOTSANE, LIM
from gen_ir246 import TOP, BADL, EX

COND = {
    'n': lambda y: f'if ((unsigned)addr != lim) {{ out = (unsigned)addr >= lim; if (out <= 0) {y} }}',
}
TAILS = {
    # goto for the good case, else goto notSane
    'h1': lambda e: f'''if (bad > 0) {{ o = addr != 0x800; if (o > 0) goto use3000; {L38} }} else {{ {e} }}
 check: lim = {LIM};
 if ((unsigned)addr != lim) {{ out = (unsigned)addr >= lim; if (out <= 0) goto load; }}
 goto notSane;
{BADL} use3000: {L30} goto check;
 load: loadSmc(addr, size); return;
 notSane: {NOTSANE} return; }}''',
    'h2': lambda e: f'''if (bad > 0) {{ o = addr != 0x800; if (o > 0) goto use3000; {L38} }} else {{ {e} }}
 check: lim = {LIM};
 if ((unsigned)addr == lim) goto notSane;
 out = (unsigned)addr >= lim; if (out > 0) goto notSane;
 goto load;
{BADL} use3000: {L30} goto check;
 load: loadSmc(addr, size); return;
 notSane: {NOTSANE} return; }}''',
    'h3': lambda e: f'''if (bad > 0) {{ o = addr != 0x800; if (o > 0) goto use3000; {L38} }} else {{ {e} }}
 check: lim = {LIM};
 if ((unsigned)addr != lim) {{ out = (unsigned)addr >= lim; if (out <= 0) goto load; }}
 goto notSane;
{BADL} use3000: {L30} goto check;
 notSane: {NOTSANE} return;
 load: loadSmc(addr, size); return; }}''',
    # flag for the check, tested later
    'h4': lambda e: f'''if (bad > 0) {{ o = addr != 0x800; if (o > 0) goto use3000; {L38} }} else {{ {e} }}
 check: lim = {LIM};
 if ((unsigned)addr != lim) {{ out = (unsigned)addr >= lim; if (out <= 0) {{ loadSmc(addr, size); return; }} }}
 goto notSane;
{BADL} use3000: {L30} goto check;
 notSane: {NOTSANE} return; }}''',
}
forms = {k: TOP + f(EX['c9']) for k, f in TAILS.items()}

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
