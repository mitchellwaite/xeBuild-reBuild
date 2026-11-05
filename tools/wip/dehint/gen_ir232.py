"""Attempt 17: one extra name freed after dce3's size-test deletions (second try): forms of bad, o, ok and t."""
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ir17lib import *
SAN = 'loadSmc(addr, size); return;'
def body(okd, tf, bf, of):
    return f'''{ATTR}void getImageSmc(void)
{{
{HEAD} {okd}
 unsigned t;
 int bad, o;
 if (ok <= 0) {{
 {LOG0} addr = 0x1000;
 }}
 {tf}
 fixSize:
 {bf}
 if (bad > 0) {{
 {of}
 if (o <= 0) {{ {L38} }} else {{ {L30} }}
 }} else {{
 __asm__("" : "+D"(addr));
 }}
 {{
 unsigned lim = {LIM};
 if ((unsigned)addr != lim) {{ int out = (unsigned)addr >= lim; if (out <= 0) {{ {SAN} }} }}
 }}
 {NOTSANE}
 return;
 badAddr:
 {LOG0} addr = 0x1000;
 goto fixSize;
}}'''
OK = {'a': 'int ok = addr != 0;', 'b': 'int z = !addr; int ok = !z;', 'c': 'int ok = addr ? 1 : 0;', 'd': 'int ok = !!addr;', 'e': 'int ok = 0; if (addr) ok = 1;'}
TF = {'a': 't = addr; if (t != 0x1000) { if (t != 0x800) goto badAddr; }',
      'b': 't = addr; if (t != 0x1000) { unsigned t2 = addr; if (t2 != 0x800) goto badAddr; }',
      'c': 't = addr; { int n1 = t != 0x1000; if (n1) { if (t != 0x800) goto badAddr; } }',
      'd': 't = addr; { int n1 = t != 0x1000; int n2 = t != 0x800; if (n1) { if (n2) goto badAddr; } }',
      'e': 't = addr; { int n2 = t != 0x800; if (t != 0x1000) { if (n2) goto badAddr; } }',
      'f': 't = addr; if (t != 0x1000) { int n2 = t != 0x800; if (n2) goto badAddr; }',
      }
BF = {'a': 'bad = size != 0x3000 && size != 0x3800;', 'b': 'bad = (size != 0x3000) & (size != 0x3800);', 'c': 'bad = !(size == 0x3000 || size == 0x3800);',
      'd': '{ int b1 = size != 0x3000; int b2 = size != 0x3800; bad = b1 && b2; }', 'e': '{ int b1 = size != 0x3000; int b2 = size != 0x3800; bad = b1 & b2; }',
      'f': '{ int g = size == 0x3000 || size == 0x3800; bad = !g; }'}
OF = {'a': 'o = addr != 0x800;', 'b': '{ int is = addr == 0x800; o = !is; }', 'c': 'o = (unsigned)addr != 0x800;', 'd': 'o = !(addr == 0x800);', 'e': 'o = 1; if (addr == 0x800) o = 0;'}
forms = {}
for a, b, c, d in itertools.product(OK, TF, BF, OF):
    forms[a + b + c + d] = body(OK[a], TF[b], BF[c], OF[d])
if __name__ == '__main__':
    print(len(forms))
    r = sweep(forms, top=25)
