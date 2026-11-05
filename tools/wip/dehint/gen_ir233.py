"""Attempt 17: more flags with `> 0`/`<= 0` (they stay until ccp3/forwprop3, so they do push names on the stack): T's tests and the outer sane test."""
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_ir232 import *
def body2(tf, san):
    return f'''{ATTR}void getImageSmc(void)
{{
{HEAD} int ok = addr != 0;
 unsigned t;
 int bad, o;
 if (ok <= 0) {{
 {LOG0} addr = 0x1000;
 }}
 {tf}
 fixSize:
 bad = size != 0x3000 && size != 0x3800;
 if (bad > 0) {{
 o = addr != 0x800;
 if (o <= 0) {{ {L38} }} else {{ {L30} }}
 }} else {{
 __asm__("" : "+D"(addr));
 }}
 {{
 unsigned lim = {LIM};
 {san}
 }}
 {NOTSANE}
 return;
 badAddr:
 {LOG0} addr = 0x1000;
 goto fixSize;
}}'''
A = '(unsigned)addr'
TF2 = {
 'p': 't = addr; if (t != 0x1000) { if (t != 0x800) goto badAddr; }',
 'n2': 't = addr; if (t != 0x1000) { int n2 = t != 0x800; if (n2 > 0) goto badAddr; }',
 'n1': 't = addr; { int n1 = t != 0x1000; if (n1 > 0) { if (t != 0x800) goto badAddr; } }',
 'n12': 't = addr; { int n1 = t != 0x1000; if (n1 > 0) { int n2 = t != 0x800; if (n2 > 0) goto badAddr; } }',
 'm2': 't = addr; if (t != 0x1000) { int n2 = t != 0x800; if (n2 <= 0) goto fixSize; goto badAddr; }',
 'm1': 't = addr; { int n1 = t != 0x1000; if (n1 <= 0) goto fixSize; if (t != 0x800) goto badAddr; }',
}
SN = {
 'p': f'if ({A} != lim) {{ int out = {A} >= lim; if (out <= 0) {{ {SAN} }} }}',
 'd': f'{{ int d = {A} != lim; if (d > 0) {{ int out = {A} >= lim; if (out <= 0) {{ {SAN} }} }} }}',
 'e': f'{{ int d = {A} == lim; if (d <= 0) {{ int out = {A} >= lim; if (out <= 0) {{ {SAN} }} }} }}',
 'f': f'{{ int d = {A} != lim; if (d > 0) {{ if ({A} < lim) {{ {SAN} }} }} }}',
 'g': f'{{ int d = {A} == lim; if (d <= 0) {{ if ({A} < lim) {{ {SAN} }} }} }}',
 'h': f'if ({A} != lim) {{ if ({A} < lim) {{ {SAN} }} }}',
 'i': f'if ({A} != lim) {{ int in = {A} < lim; if (in > 0) {{ {SAN} }} }}',
}
forms = {a + '.' + b: body2(TF2[a], SN[b]) for a, b in itertools.product(TF2, SN)}
if __name__ == '__main__':
    sweep(forms, top=45)
