# gen.py NAME EDIT... : v/NAME.c from c0.c (plain) with named equivalent edits
import sys
s = open('c0.c').read()
def rep(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b, 1)
EB0 = s[s.index('\tuint32_t block = myatoh32(sblock, -1);'):s.index("/* the option's")]
def grab(key):
    i = EB0.index(key); i = EB0.rindex('log_printf', 0, i); return EB0[i:EB0.index(';', i) + 1]
L_F = grab('Failed'); L_O = grab('outside'); L_I = grab('Invalid'); L_E = grab('erasing'); L_S = grab('Success')
H = '\tuint32_t block = myatoh32(sblock, -1);\n'
LIM = 'cinfo->nandSize / cinfo->blockSize'
BODIES = {
 # invert outer
 'B1': H + '\tif (block == -1) {\n\t\t%s\n\t\treturn;\n\t}\n\tif (block < %s) {\n\t\t%s\n\t\tif (netEraseBlockU32(block, 1))\n\t\t\t%s\n\t\telse\n\t\t\t%s\n\t} else\n\t\t%s\n}\n\n' % (L_I, LIM, L_E, L_S, L_F, L_O),
 # invert inner
 'B2': H + '\tif (block != -1) {\n\t\tif (block >= %s)\n\t\t\t%s\n\t\telse {\n\t\t\t%s\n\t\t\tif (!netEraseBlockU32(block, 1))\n\t\t\t\t%s\n\t\t\telse\n\t\t\t\t%s\n\t\t}\n\t} else\n\t\t%s\n}\n\n' % (LIM, L_O, L_E, L_F, L_S, L_I),
 # invert both
 'B3': H + '\tif (block == -1)\n\t\t%s\n\telse if (block >= %s)\n\t\t%s\n\telse {\n\t\t%s\n\t\tif (!netEraseBlockU32(block, 1))\n\t\t\t%s\n\t\telse\n\t\t\t%s\n\t}\n}\n\n' % (L_I, LIM, L_O, L_E, L_F, L_S),
 # invert success test only
 'B4': H + '\tif (block != -1) {\n\t\tif (block < %s) {\n\t\t\t%s\n\t\t\tif (!netEraseBlockU32(block, 1))\n\t\t\t\t%s\n\t\t\telse\n\t\t\t\t%s\n\t\t} else\n\t\t\t%s\n\t} else\n\t\t%s\n}\n\n' % (LIM, L_E, L_F, L_S, L_O, L_I),
 # early returns
 'B5': H + '\tif (block == -1) { %s return; }\n\tif (block >= %s) { %s return; }\n\t%s\n\tif (netEraseBlockU32(block, 1)) { %s return; }\n\t%s\n}\n\n' % (L_I, LIM, L_O, L_E, L_S, L_F),
}
for e in sys.argv[2:]:
    k, _, a = e.partition('=')
    if k in BODIES: rep(EB0, BODIES[k])
    elif k == 'R':
        o, n = a.split('|'); rep(o.replace('@N', '\n').replace('@T', '\t'), n.replace('@N', '\n').replace('@T', '\t'))
    elif k == 'P': rep('#define AT(l)\n', '#define AT(l) l:\n')
    else: raise SystemExit('bad ' + k)
open('v/%s.c' % sys.argv[1], 'w', newline='\n').write(s)
