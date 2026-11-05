"""Attempt 17: `ok &&` replaced by a LIVE first test on the same compare that ifcombine merges away (combine_comparisons), so the not-sane
block still has two predecessors at profile_estimate: `if (a != lim) { if (a < lim) sane }` is `a < lim` by ifcombine, and each test can fail."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ir17lib import *

def body(sane, zset='ok = 1;', okdecl='int ok = addr != 0;', zt='ok <= 0', attr=True):
    a = ATTR if attr else ''
    return f'''{a}void getImageSmc(void)
{{
{HEAD} {okdecl}
 unsigned t;
 int bad, o;
 if ({zt}) {{
 {LOG0} addr = 0x1000; {zset}
 }}
 t = addr;
 if (t != 0x1000) {{ if (t != 0x800) goto badAddr; }}
 fixSize:
 bad = size != 0x3000 && size != 0x3800;
 if (bad > 0) {{
 o = addr != 0x800;
 if (o <= 0) {{ {L38} }} else {{ {L30} }}
 }} else {{
 __asm__("" : "+D"(addr));
 }}
 {sane}
 return;
 badAddr:
 {LOG0} addr = 0x1000;
 goto fixSize;
}}'''

T = {
 'ne_lt': ('(unsigned)addr != lim', '(unsigned)addr < lim'),
 'lt_ne': ('(unsigned)addr < lim', '(unsigned)addr != lim'),
 'le_ne': ('(unsigned)addr <= lim', '(unsigned)addr != lim'),
 'ne_le': ('(unsigned)addr != lim', '(unsigned)addr <= lim'),
 'ne_lt2': ('addr != lim', 'addr < lim'),
 'le_ne2': ('addr <= lim', 'addr != lim'),
 'ne_le2': ('addr != lim', 'addr <= lim'),
}
forms = {}
for k, (a, b) in T.items():
    for lk, ld in {'loc': f'unsigned lim = {LIM};'}.items():
        forms[k + '.if'] = body(f'{{ {ld} if ({a}) {{ if ({b}) {{ loadSmc(addr, size); return; }} }} }}\n {NOTSANE}', zset='')
        forms[k + '.good'] = body(f'{{ {ld} int good = 0; if ({a}) {{ if ({b}) good = 1; }} if (good) loadSmc(addr, size); else {NOTSANE} }}', zset='')
        forms[k + '.go'] = body(f'{{ {ld} if ({a}) {{ if ({b}) {{ loadSmc(addr, size); goto end; }} }} }}\n {NOTSANE} end: ;', zset='')
        forms[k + '.neg'] = body(f'{{ {ld} if (!({a})) goto ns; if (!({b})) goto ns; loadSmc(addr, size); return; ns: {NOTSANE} }}', zset='')
        forms[k + '.or'] = body(f'{{ {ld} if (!({a})) {{ goto ns; }} if ({b}) loadSmc(addr, size); else {{ ns: {NOTSANE} }} }}', zset='')
if __name__ == '__main__':
    sweep(forms)
