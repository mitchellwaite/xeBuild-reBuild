# attempt 18: xmalloc. Ways of calling malloc that CCP might not read as the builtin. `iw16sweep.py tools/wip/dehint/gen_iw252.py -n 40`. Plain src otherwise.
# Probes first; anything with a cast on the function is a patch, not a source (see notes).
import os
BASE = os.environ.get('IWB', 'src/image_write.c')
XM = 'void *xmalloc(size_t) __asm__("_malloc") __attribute__((malloc));\n'
AL = 'xb.raw = (uint8_t *)(mem = xmalloc(xb.rawSize));'
SD = 'int finalizeImage(void)\n'
def F(call, pre=''):
    return [(XM, ''), (AL, 'xb.raw = (uint8_t *)(mem = %s);' % call), (SD, pre + SD)]
A = [
 ('base', F('malloc(xb.rawSize)')),
 ('xm_noattr', [(XM, 'void *xmalloc(size_t) __asm__("_malloc");\n')]),
 ('sfp', F('alloc(xb.rawSize)', 'static void *(*alloc)(size_t) = malloc;\n\n')),
 ('scfp', F('alloc(xb.rawSize)', 'static void *(*const alloc)(size_t) = malloc;\n\n')),
 ('stbl', F('ops.alloc(xb.rawSize)', 'static const struct { void *(*alloc)(size_t); } ops = { malloc };\n\n')),
 ('wrap', F('allocRaw(xb.rawSize)', 'static void *allocRaw(size_t n)\n{\n	return malloc(n);\n}\n\n')),
 ('cast32', F('((void *(*)(uint32_t))malloc)(xb.rawSize)')),
 ('castkr', F('((void *(*)())malloc)(xb.rawSize)')),
 ('castint', F('((void *(*)(int))malloc)(xb.rawSize)')),
 ('castret', F('((uint8_t *(*)(size_t))malloc)(xb.rawSize)')),
 ('fnvar', F('(*malloc)(xb.rawSize)')),
 ('sfpkr', F('alloc(xb.rawSize)', 'static void *(*alloc)() = malloc;\n\n')),
 ('locfpint', F('alloc((int)xb.rawSize)', 'static void *(*alloc)() = malloc;\n\n')),
]
AXES = [A]
FLAGS = []
