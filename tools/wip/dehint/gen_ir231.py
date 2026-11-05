"""Attempt 17: one extra name freed after dce3's size-test deletions puts prephitmp on _38 (below lim_48): flag types, extra copies."""
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ir17lib import *
SAN = 'loadSmc(addr, size); return;'
def body(okt, ot, bt, outt, lk):
    return f'''{ATTR}void getImageSmc(void)
{{
{HEAD} {okt} ok = addr != 0;
 unsigned t;
 {bt} bad;
 {ot} o;
 if (ok <= 0) {{
 {LOG0} addr = 0x1000;
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
 {{
 {lk}
 if ((unsigned)addr != lim) {{ {outt} out = (unsigned)addr >= lim; if (out <= 0) {{ {SAN} }} }}
 }}
 {NOTSANE}
 return;
 badAddr:
 {LOG0} addr = 0x1000;
 goto fixSize;
}}'''
T = ('int', 'char', 'short', 'long', 'signed char', 'long long')
LK = {'a': f'unsigned lim = {LIM};', 'b': 'unsigned lim = xb.dumpPages; lim *= 528;', 'c': 'int pages = xb.dumpPages; unsigned lim = 528 * pages;', 'd': 'unsigned long long lim2 = 0; unsigned lim = 528 * xb.dumpPages;'}
forms = {}
for a, b, c, d in itertools.product(T, ('int', 'char', 'short', 'long long'), ('int', 'char', 'long long'), ('int', 'char', 'short', 'long long')):
    forms['|'.join((a, b, c, d, 'a'))] = body(a, b, c, d, LK['a'])
for k, v in LK.items():
    forms['lim' + k] = body('int', 'int', 'int', 'int', v)
if __name__ == '__main__':
    print(len(forms))
    sweep(forms, top=15)
