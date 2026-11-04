"""keysshowdae.py [file]: print daeEncrypt's reference disassembly, or file's diff to it."""
import difflib, sys
import keyslib as K
ref = K.dis(K.REF)['_daeEncrypt']
if len(sys.argv) < 2:
    print('\n'.join(ref))
else:
    o = K.compile(open(sys.argv[1], newline='').read(), ['-O3'], 'sd')
    print('MATCH' if K.same(o) else 'differ', K.fndiff(o))
    for ln in difflib.unified_diff(ref, K.dis(o)['_daeEncrypt'], lineterm='', n=1):
        print(ln)
