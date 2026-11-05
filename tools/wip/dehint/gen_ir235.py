"""Attempt 18: values VRP1 can't see through.  Struct/array holding addr and size, loadSmc through a pointer (memory until
IPA + sra), helpers by value or pointer for the checks, E statements through a second variable.  Attribute and pin in a lattice."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ir17lib, irlib
from ir17lib import base, score, A, B, L0, LOG0, L38, L30, NOTSANE, HEAD, ATTR, LIM

LOADSMC = base[L0:base.index('/* One optimize attribute')]
PIN = '__asm__("" : "+D"(addr));'


def text(fn, pre=None):
    """whole file, fn replaces getImageSmc, pre (if given) replaces loadSmc"""
    t = base[:A] + fn + '\n' + base[B:]
    if pre is not None:
        t = t.replace(LOADSMC, pre + '\n')
    return t


def ls_ptr(ty='struct smcArea', a='s->addr', z='s->size'):
    x = LOADSMC.replace('static void loadSmc(int addr, int size)', 'struct smcArea { int addr, size; };\nstatic void loadSmc(struct smcArea *s)')
    x = x.replace('malloc(size)', f'malloc({z})').replace('xb.smc.size = size', f'xb.smc.size = {z}')
    x = x.replace('xb.dump + addr, size', f'xb.dump + {a}, {z}').replace('\\n", addr, size);', f'\\n", {a}, {z});')
    x = x.replace('not using...\\n", size);', f'not using...\\n", {z});')
    return x


def ls_2ptr():
    x = LOADSMC.replace('static void loadSmc(int addr, int size)', 'static void loadSmc(int *addr, int *size)')
    x = x.replace('malloc(size)', 'malloc(*size)').replace('xb.smc.size = size', 'xb.smc.size = *size')
    x = x.replace('xb.dump + addr, size', 'xb.dump + *addr, *size').replace('\\n", addr, size);', '\\n", *addr, *size);')
    x = x.replace('not using...\\n", size);', 'not using...\\n", *size);')
    return x


SAN0 = 'loadSmc(addr, size);'


def body(att, els, sanecall='loadSmc(addr, size);', decl='', hd=HEAD, addr='addr', size='size', seta=None, sets=None, cmpa=None, t0='t = addr;', badset=''):
    """the current shape with addr, size spelled through names"""
    cmpa = cmpa or f'(unsigned){addr}'
    seta = seta or (lambda v: f'{addr} = {v};')
    sets = sets or (lambda v: f'{size} = {v};')
    l0 = LOG0.replace('addr);', addr + ');')
    l38 = sets('0x3800') + '\n' + L38.split('\n')[1].replace('size);', size + ');') + '\n'
    l30 = sets('0x3000') + '\n' + L30.split('\n')[1].replace('size);', size + ');') + '\n'
    ns = NOTSANE.replace('addr, size);', f'{addr}, {size});')
    return f'''{att}void getImageSmc(void)
{{
{hd} {decl}
 int ok = {addr} != 0;
 unsigned t, lim;
 int wrong, bad, o, out;
 if (ok <= 0) {{
 {l0} {seta('0x1000')}
 }}
 {t0}
 if (t != 0x1000) {{
 wrong = t != 0x800;
 if (wrong > 0) goto badAddr;
 }}
fixSize:
 bad = {size} != 0x3000 && {size} != 0x3800;
 if (bad > 0) {{
 o = {addr} != 0x800;
 if (o <= 0) {{ {l38} }} else {{ {l30} }}
 }} else {{
 {els}
 }}
 lim = {LIM};
 if ({cmpa} != lim) {{
 out = {cmpa} >= lim;
 if (out <= 0) {{ {sanecall} return; }}
 }}
 {ns} return;
badAddr:
 {l0} {seta('0x1000')} {badset}
 goto fixSize;
}}'''


HS = 'struct flashhdr *h = (struct flashhdr *)xb.dump;\n'
forms = {}
ATTS = {'a3': ATTR, 'a0': ''}
for ak, at in ATTS.items():
    for pk, p in (('np', ';'), ('pin', PIN)):
        forms['base.%s.%s' % (ak, p and pk)] = (body(at, p), None)
    # struct through a pointer: all spellings go through memory until the IPA inline, sra at 109 scalarises
    sb = HS + 'struct smcArea s;\n s.addr = SWAP32(h->smcBootAddr);\n s.size = SWAP32(h->smcBootSize);\n'
    forms['st.all.%s' % ak] = (body(at, ';', 'loadSmc(&s);', hd=sb, addr='s.addr', size='s.size', t0='t = s.addr;'), ls_ptr())
    # only the size arms and else write the struct
    forms['st.join.%s' % ak] = (body(at, 's.addr = addr; s.size = size;', 'loadSmc(&s);', decl='struct smcArea s;',
                                     sets=lambda v: f'size = {v}; s.size = size; s.addr = addr;', cmpa='(unsigned)s.addr'), ls_ptr())
    forms['st.join2.%s' % ak] = (body(at, 's.addr = addr; s.size = size;', 'loadSmc(&s);', decl='struct smcArea s;',
                                      sets=lambda v: f'size = {v}; s.size = size; s.addr = addr;'), ls_ptr())
    forms['st.join3.%s' % ak] = (body(at, 's.addr = addr;', 'loadSmc(&s);', decl='struct smcArea s;',
                                      sets=lambda v: f'size = {v}; s.addr = addr;', hd=HEAD).replace('loadSmc(&s);', 's.size = size; loadSmc(&s);'), ls_ptr())
    # two scalars by pointer (addressable until ccp2)
    forms['pp.%s' % ak] = (body(at, ';', 'loadSmc(&addr, &size);'), ls_2ptr())
    forms['pp.pin.%s' % ak] = (body(at, PIN, 'loadSmc(&addr, &size);'), ls_2ptr())
    # second variable in E
    forms['e.addr_t.%s' % ak] = (body(at, 'addr = t;', badset='t = 0x1000;'), None)
    forms['e.addr_t2.%s' % ak] = (body(at, 'addr = (int)t;', badset='t = addr;'), None)
    forms['e.t_addr.%s' % ak] = (body(at, 't = addr;', cmpa='t', sets=lambda v: f'size = {v}; t = addr;'), None)
    forms['e.t_addr2.%s' % ak] = (body(at, 't = addr;', cmpa='t', badset='t = 0x1000;'), None)
    forms['e.t_addr3.%s' % ak] = (body(at, 't = addr;', badset='t = 0x1000;', cmpa='t'), None)
    # array
    forms['arr.%s' % ak] = (body(at, ';', 'loadSmc(&s);', hd=sb, addr='s.addr', size='s.size', t0='t = s.addr;').replace('struct smcArea s;', 'struct smcArea s[1];').replace('s.addr', 's->addr').replace('s.size', 's->size').replace('&s', 's'), ls_ptr())

if __name__ == '__main__':
    res = []
    for k, (f, pre) in forms.items():
        s = score(text(f, pre))
        if s[0] == 'E':
            print(k, 'ERR', s[1][:300])
            continue
        res.append((s[1], s[0], k, s[2], s[3]))
    for r in sorted(res, key=lambda x: (x[0], x[1])):
        print(r)
