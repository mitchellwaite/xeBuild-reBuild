"""One source function: head form x where key/hash live x test sense x return form."""
import itertools
from gen_dv1 import VD

BODY = '''memset(key, 0, 16);
XeCryptHmacSha(key, 16, seg, 32, 0, 0, 0, 0, hash, 20);
ok = XeKeysPkcs1Verify(hash, seg + 32, (const XECRYPT_RSA *)xb.pubPirs);
'''
TEST = {
    'ifok': '''if (ok)
	log_printf(1, "sig %d good! ", n);
else
	log_printf(1, "\\nsig %d FAIL! ", n);
''',
    'ifnot': '''if (!ok)
	log_printf(1, "\\nsig %d FAIL! ", n);
else
	log_printf(1, "sig %d good! ", n);
''',
}
DECL = '''uint8_t key[16];
uint8_t hash[20];
'''


def ind(s, n=1):
    return ''.join('\t' * n + l + '\n' if l else '\n' for l in s.split('\n')[:-1])


def shape(head, scope, test):
    inner = BODY + TEST[test]
    sig = 'int daeVerifySig(uint8_t *seg, uint32_t size, int n)\n{\n'
    if head == 'nest1':	 # int ok = 1; if (pub && size >= 288) { ... } return ok;
        s = sig
        if scope == 'fn':
            s += ind(DECL)
        s += '\tint ok = 1;\n\n\tif (xb.pubPirs && size >= 288) {\n'
        if scope != 'fn':
            s += ind(DECL, 2) + '\n'
        s += ind(inner, 2) + '\t}\n\treturn ok;\n}\n'
    elif head == 'nest2':	 # nested ifs
        s = sig
        if scope == 'fn':
            s += ind(DECL)
        s += '\tint ok = 1;\n\n\tif (xb.pubPirs) {\n\t\tif (size >= 288) {\n'
        if scope != 'fn':
            s += ind(DECL, 3) + '\n'
        s += ind(inner, 3) + '\t\t}\n\t}\n\treturn ok;\n}\n'
    elif head == 'set':	 # ok = 1 in the else
        s = sig
        if scope == 'fn':
            s += ind(DECL)
        s += '\tint ok;\n\n\tif (xb.pubPirs && size >= 288) {\n'
        if scope != 'fn':
            s += ind(DECL, 2) + '\n'
        s += ind(inner, 2) + '\t} else\n\t\tok = 1;\n\treturn ok;\n}\n'
    elif head == 'early':	 # returns, then a block for the signature
        s = sig
        if scope == 'fn':
            s += ind(DECL)
        s += '\tint ok;\n\n\tif (!xb.pubPirs)\n\t\treturn 1;\n\tif (size < 288)\n\t\treturn 1;\n'
        if scope == 'fn':
            s += ind(inner) + '\treturn ok;\n}\n'
        else:
            s += '\t{\n' + ind(DECL, 2) + '\n' + ind(inner, 2) + '\t}\n\treturn ok;\n}\n'
    elif head == 'earlyor':
        s = sig
        if scope == 'fn':
            s += ind(DECL)
        s += '\tint ok;\n\n\tif (!xb.pubPirs || size < 288)\n\t\treturn 1;\n'
        if scope == 'fn':
            s += ind(inner) + '\treturn ok;\n}\n'
        else:
            s += '\t{\n' + ind(DECL, 2) + '\n' + ind(inner, 2) + '\t}\n\treturn ok;\n}\n'
    return s


def variants():
    for h, sc, t in itertools.product(['nest1', 'nest2', 'set', 'early', 'earlyor'], ['fn', 'in'], TEST):
        yield '%s|%s|%s' % (h, sc, t), shape(h, sc, t) + VD
