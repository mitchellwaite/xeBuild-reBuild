"""Attempt 18: helpers inlined at IPA (by value, by pointer, returning a struct), a switch on addr, do-while(0), each with the E forms
none / pin / t_addr (t = addr at the end of each size arm and in else, t read by the bound test), attribute a3 and a0."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_ir235 import *

Z = 'if (ok <= 0) {\n ' + LOG0 + ' addr = 0x1000;\n }'
TESTS = {
 'nest': lambda bad: f't = addr; if (t != 0x1000) {{ wrong = t != 0x800; if (wrong > 0) {{ {bad} }} }}',
 'sw': lambda bad: f't = addr; switch (t) {{ case 0x800: case 0x1000: break; default: {bad} }}',
 'swi': lambda bad: f't = addr; switch (addr) {{ case 0x800: case 0x1000: break; default: {bad} }}',
 'dw': lambda bad: f't = addr; do {{ if (t == 0x1000) break; wrong = t != 0x800; if (wrong <= 0) break; {bad} }} while (0);',
}
BADV = LOG0 + ' addr = 0x1000;'
E = {'none': (';', '', '(unsigned)addr'), 'pin': (PIN, '', '(unsigned)addr'), 'ta': ('t = addr;', ' t = addr;', 't')}
SIZE = lambda set_t, els: f'''bad = size != 0x3000 && size != 0x3800;
 if (bad > 0) {{
 o = addr != 0x800;
 if (o <= 0) {{ {L38} {set_t} }} else {{ {L30} {set_t} }}
 }} else {{
 {els}
 }}'''
SIZESW = lambda set_t, els: f'''bad = size != 0x3000 && size != 0x3800;
 if (bad > 0) {{
 switch (addr) {{ case 0x800: {L38} {set_t} break; default: {L30} {set_t} break; }}
 }} else {{
 {els}
 }}'''
TAIL = lambda c, san='loadSmc(addr, size);': f'''lim = {LIM};
 if ({c} != lim) {{
 out = {c} >= lim;
 if (out <= 0) {{ {san} return; }}
 }}
 {NOTSANE} return;'''
DECL = 'int ok = addr != 0;\n unsigned t, lim;\n int wrong, bad, o, out;\n'
forms = {}
for ak, at in (('a3', ATTR), ('a0', '')):
    for ek, (els, st, c) in E.items():
        # 1. test forms inline, bad arm in line (no labels) and bad arm at the end
        for tk, tf in TESTS.items():
            for szk, sz in (('sz', SIZE), ('szw', SIZESW)):
                k = '.'.join((tk, szk, ek, ak))
                forms['in.' + k] = (f'{at}void getImageSmc(void)\n{{\n{HEAD} {DECL} {Z}\n {tf(BADV)}\n {sz(st, els)}\n {TAIL(c)}\n}}', None)
                forms['lab.' + k] = (f'{at}void getImageSmc(void)\n{{\n{HEAD} {DECL} {Z}\n {tf("goto badAddr;")}\n fixSize:\n {sz(st, els)}\n {TAIL(c)}\n badAddr:\n {BADV}\n goto fixSize;\n}}', None)
        # 2. switch for zero and the two good values together
        forms['sw3.' + ek + '.' + ak] = (f'{at}void getImageSmc(void)\n{{\n{HEAD} {DECL} switch (addr) {{ case 0x800: case 0x1000: break; case 0: {BADV} break; default: {BADV} break; }}\n {SIZE(st, els)}\n {TAIL(c)}\n}}', None)
        forms['sw4.' + ek + '.' + ak] = (f'{at}void getImageSmc(void)\n{{\n{HEAD} {DECL} switch (addr) {{ case 0: {BADV} break; case 0x800: case 0x1000: break; default: {BADV} break; }}\n {SIZE(st, els)}\n {TAIL(c)}\n}}', None)
        # 3. helpers, by value: IPA inlined
        hv = f'''static int smcFixAddr(int addr)
{{
 int ok = addr != 0; unsigned t; int wrong;
 {Z}
 t = addr; if (t != 0x1000) {{ wrong = t != 0x800; if (wrong > 0) {{ {BADV} }} }}
 return addr;
}}
'''
        hs = f'''static int smcFixSize(int addr, int size)
{{
 int bad = size != 0x3000 && size != 0x3800, o;
 if (bad > 0) {{ o = addr != 0x800; if (o <= 0) {{ {L38} }} else {{ {L30} }} }}
 return size;
}}
'''
        hp = hs.replace('int smcFixSize(int addr, int size)', 'void smcFixSize(int addr, int *ps)').replace('int bad = size', 'int size = *ps; int bad = size').replace('return size;', '*ps = size;')
        hpa = hv.replace('int smcFixAddr(int addr)', 'void smcFixAddr(int *pa)').replace('int ok = addr', 'int addr = *pa; int ok = addr').replace('return addr;', '*pa = addr;')
        d2 = 'unsigned t, lim;\n int out;\n'
        if ek == 'none':
            forms['hv.' + ak] = (f'{hv}{hs}{at}void getImageSmc(void)\n{{\n{HEAD} {d2} addr = smcFixAddr(addr);\n size = smcFixSize(addr, size);\n {TAIL(c)}\n}}', None)
            forms['hva.' + ak] = (f'{hv}{at}void getImageSmc(void)\n{{\n{HEAD} {d2} int bad, o;\n addr = smcFixAddr(addr);\n {SIZE("", ";")}\n {TAIL(c)}\n}}', None)
            forms['hvs.' + ak] = (f'{hs}{at}void getImageSmc(void)\n{{\n{HEAD} {DECL} {Z}\n {TESTS["nest"](BADV)}\n size = smcFixSize(addr, size);\n {TAIL(c)}\n}}', None)
            forms['hps.' + ak] = (f'{hp}{at}void getImageSmc(void)\n{{\n{HEAD} {DECL} {Z}\n {TESTS["nest"](BADV)}\n smcFixSize(addr, &size);\n {TAIL(c)}\n}}', None)
            forms['hpa.' + ak] = (f'{hpa}{at}void getImageSmc(void)\n{{\n{HEAD} {d2} int bad, o;\n smcFixAddr(&addr);\n {SIZE("", ";")}\n {TAIL(c)}\n}}', None)
            forms['hpp.' + ak] = (f'{hpa}{hp}{at}void getImageSmc(void)\n{{\n{HEAD} {d2} smcFixAddr(&addr);\n smcFixSize(addr, &size);\n {TAIL(c)}\n}}', None)
            hst = 'struct smcArea { int addr, size; };\n' + f'''static struct smcArea smcFix(struct smcArea s)
{{
 int addr = s.addr, size = s.size;
 int ok = addr != 0; unsigned t; int wrong, bad, o;
 {Z}
 t = addr; if (t != 0x1000) {{ wrong = t != 0x800; if (wrong > 0) {{ {BADV} }} }}
 {SIZE("", ";")}
 s.addr = addr; s.size = size;
 return s;
}}
'''
            forms['hst.' + ak] = (f'{hst}{at}void getImageSmc(void)\n{{\n{HS} struct smcArea s; int addr, size; {d2} s.addr = SWAP32(h->smcBootAddr); s.size = SWAP32(h->smcBootSize); s = smcFix(s); addr = s.addr; size = s.size;\n {TAIL(c)}\n}}', None)

if __name__ == '__main__':
    res = []
    for k, (f, pre) in forms.items():
        s = score(text(f, pre))
        if s[0] == 'E':
            print(k, 'ERR', s[1][:300])
            continue
        res.append((s[1], s[0], k, s[3]))
    print(len(res))
    for r in sorted(res, key=lambda x: (x[0], x[1]))[:40]:
        print(r)
