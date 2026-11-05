"""Attempt 17, measurement: is the reference's E (conversion in the size-ok block, `mov edi,0x1000; mov ebx,edi`) what comes out when the
size test's join isn't threaded until after PRE?  Function-only pass disables, no hint in the source (measurement only, nothing lands)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ir17lib import *

def form(sane, arm, t, zero):
    return f'''void getImageSmc(void)
{{
{HEAD} {zero[0]}
 unsigned t;
 int bad, o;
 if ({zero[1]}) {{
 {LOG0} addr = 0x1000; {zero[2]}
 }}
 t = addr;
 {t}
 fixSize:
 bad = size != 0x3000 && size != 0x3800;
 if (bad > 0) {{
 {arm}
 }}
 {sane}
 return;
 badAddr:
 {LOG0} addr = 0x1000;
 goto fixSize;
}}'''

ZERO = {'okf': ('int ok = addr != 0;', 'ok <= 0', 'ok = 1;'), 'pl': ('', '!addr', '')}
TT = {'t6': 'if (t != 0x1000) { if (t != 0x800) goto badAddr; }'}
ARM = {'o': f'o = addr != 0x800; if (o <= 0) {{ {L38} }} else {{ {L30} }}',
       'u': f'if ((unsigned)addr == 0x800) {{ {L38} }} else {{ {L30} }}'}
SANE = {'ok': f'if (ok && addr < {LIM}) loadSmc(addr, size); else {NOTSANE}',
        'pl': f'if (addr < {LIM}) loadSmc(addr, size); else {NOTSANE}'}
FN = 'getImageSmc'
FL = {
    '': (),
    '.nov1': ('-fdisable-tree-vrp1=' + FN,),
    '.nod2': ('-fdisable-tree-dom2=' + FN,),
    '.no12': ('-fdisable-tree-vrp1=' + FN, '-fdisable-tree-dom2=' + FN),
}
forms = {}
for zk, z in ZERO.items():
    for tk, t in TT.items():
        for ak, a in ARM.items():
            for sk, s in SANE.items():
                if sk == 'ok' and zk != 'okf':
                    continue
                forms['.'.join((zk, tk, ak, sk))] = form(s, a, t, z)
if __name__ == '__main__':
    sweep(forms, list(FL.items()))
