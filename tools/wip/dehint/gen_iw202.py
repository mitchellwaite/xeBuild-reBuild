# attempt 13: writeFsTable on the bitfield family. Dead test and attribute each kept or gone, call forms (goto, if/else either way),
# the length's spelling. As the Linux build reads: if (xb.bigBlock) imgAdd(off, buf, 0x4000, 0x2c, 0x1ffe, 0); else ...
import os
BASE = os.environ.get('IWB', 'build/iw/a13/n8_bf.c')
ATTR = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
DEAD = '''	if ((off & 0x3fff) > 0x3fff)
		off += 0x4000;
'''
CM = '''	/* dead (VRP1 removes it): only sets which SSA names get recycled in the two
	   inlined imgAdd copies, which decides the big copy's page-loop compares.
	   It's here, not in imgAdd, so that it can't touch the clones */
'''
CALLS = '''	if (!xb.bigBlock)
		goto small;
	imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);
	goto done;
small:
	imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);
done:
'''
def C(form, n):
    B = '	imgAdd(off, buf, %s, 0x2c, 0x1ffe, 0);\n' % n
    S = '	imgAdd(off, buf, %s, 0x30, 0x1ffd, 0);\n' % n
    return ['	if (!xb.bigBlock)\n		goto small;\n' + B + '	goto done;\nsmall:\n' + S + 'done:\n',
            '	if (xb.bigBlock)\n	' + B + '	else\n	' + S,
            '	if (!xb.bigBlock)\n	' + S + '	else\n	' + B,
            '	if (xb.bigBlock)\n		goto big;\n' + S + '	goto done;\nbig:\n' + B + 'done:\n'][form]
AXES = [
 [('', []), ('noattr', [(ATTR, 'void writeFsTable')])],
 [('', []), ('nodead', [(CM, ''), (DEAD, '')])],
 [(('c%dn%d' % (f, k)), [(CALLS, C(f, n))]) for f in range(4) for k, n in enumerate(['i * 0x400', '0x4000', 'p - buf'])],
]
FLAGS = []
