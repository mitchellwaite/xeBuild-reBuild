"""getImageSmc from gen_ir155's near miss + attribute: window for P(size bad) is [53, 70] (measured).  Forms of the size test with the opcode-positive predictor (64) on a flag VRP folds later."""
FOCUS = ['_getImageSmc']
BASE = 'build/ir/a10/xa3.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('void getImageSmc(void)')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
S3800 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);\n'
S3000 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);\n'
ARM = f'if (addr == 0x800) {{ size = 0x3800; {S3800} }} else {{ size = 0x3000; {S3000} }}'
PIN = '__asm__("" : "+D"(addr));'
k = OLD.index('if (size != 0x3000')
e = OLD.index('if (t && addr')
SZ = OLD[k:e]
def N(a, b, ta='int', pa='> 0', pb='> 0', tv='size'):
    return f"""{{ {ta} n1 = {tv} != {a}; {ta} n2 = {tv} != {b}; if (n1 {pa}) {{ if (n2 {pb}) {{ {ARM} goto sz; }} }} {PIN} sz:; }}
"""
FORMS = {}
for (la, a, b) in (('38', '0x3800', '0x3000'), ('30', '0x3000', '0x3800')):
    FORMS['nn' + la] = N(a, b)
    FORMS['nb' + la] = N(a, b, pb='!= 0')
    FORMS['nc' + la] = N(a, b, pa='!= 0')
    FORMS['s' + la] = f"""{{ int n1 = size != {a}; if (n1 > 0) {{ int n2 = size != {b}; if (n2 > 0) {{ {ARM} goto sz; }} }} {PIN} sz:; }}
"""
    FORMS['u' + la] = f"""{{ unsigned s = size; int n1 = s != {a}; int n2 = s != {b}; if (n1 > 0) {{ if (n2 > 0) {{ {ARM} goto sz; }} }} {PIN} sz:; }}
"""
    FORMS['e' + la] = f"""{{ int n1 = size != {a}; int n2 = size != {b}; if (n1 > 0) {{ if (n2 > 0) {{ {ARM} }} else {{ {PIN} }} }} else {{ {PIN} }} }}
"""
    FORMS['m' + la] = f"""{{ int n1 = size != {a}; if (n1 > 0) {{ if (size != {b}) {{ {ARM} goto sz; }} }} {PIN} sz:; }}
"""
AX = [(k2, [(SZ, v)]) for k2, v in FORMS.items()]
AXES = [AX]
