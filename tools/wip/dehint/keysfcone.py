"""keysfcone.py <shape> [nopure]: print the _fcrtEncrypt diff for one keysfc shape."""
import difflib, sys
import keyslib as K
import keysfc as F

name = sys.argv[1]
b = K.base()
if 'nopure' in sys.argv:
    b = b.replace('uint32_t getBeU32(const uint8_t *p) __attribute__((pure));\n', '')
decl, body = F.SHAPES[name]
s = F.fnreplace(b, F.HEAD % (('\t' + decl) if decl else '', body))
o = K.compile(s, tag='fcone')
print(K.same(o), K.fndiff(o))
for ln in difflib.unified_diff(K.dis(K.REF)['_fcrtEncrypt'], K.dis(o)['_fcrtEncrypt'], lineterm='', n=1):
    print(ln)
