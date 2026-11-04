# attempt 18: xmalloc. gen_iw252 found a non-builtin call without the asm label: an argument whose type isn't size_t's, through a type with no prototype or `int` (gimple_call_builtin_p's arg check is inferred: source not read).
# Which spellings reach that? `iw16sweep.py tools/wip/dehint/gen_iw253.py -n 40`.
import os
BASE = os.environ.get('IWB', 'src/image_write.c')
XM = 'void *xmalloc(size_t) __asm__("_malloc") __attribute__((malloc));\n'
AL = 'xb.raw = (uint8_t *)(mem = xmalloc(xb.rawSize));'
INC = '#include <stdlib.h>\n'
WF = 'buf = malloc(0x4000);'
def F(call, decl='', wf=None, inc=None):
    e = [(XM, decl), (AL, 'xb.raw = (uint8_t *)(mem = %s);' % call)]
    if wf: e.append((WF, wf))
    if inc is not None: e.append((INC, inc))
    return e
A = [
 ('castint', F('((void *(*)(int))malloc)(xb.rawSize)')),
 ('castint_wf', F('((void *(*)(int))malloc)(xb.rawSize)', wf='buf = ((void *(*)(int))malloc)(0x4000);')),
 ('kr_withinc', F('malloc((int)xb.rawSize)', 'void *malloc();\n')),
 ('kr_noinc', F('malloc((int)xb.rawSize)', 'void *malloc();\nvoid free();\n', inc='')),
 ('kr_noinc_u', F('malloc(xb.rawSize)', 'void *malloc();\nvoid free();\n', inc='')),
 ('impl', F('malloc((int)xb.rawSize)', '', inc='')),
 ('intproto', F('malloc(xb.rawSize)', 'void *malloc(int);\nvoid free(void *);\n', inc='')),
 ('intproto_a', F('malloc(xb.rawSize)', 'void *malloc(int) __attribute__((malloc));\nvoid free(void *);\n', inc='')),
 ('xb_cast', F('((void *(*)())malloc)((int)xb.rawSize)')),
 ('xb_cast2', F('(*(void *(*)())malloc)((int)xb.rawSize)')),
]
AXES = [A]
FLAGS = []
