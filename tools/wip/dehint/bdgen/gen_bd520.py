"""Attempt 40: attempt 39's inlining refusals redone so that loadBl stays inlined.  The refusal is ipa-inline's early
min_size check (want_inline_small_function_p: min_size - call size > max(insns-single, insns-auto) -> "max-inline-insns-auto
limit reached"); min_size is the size not under a predicate, and only a switch on an unmodified load of the parameter's
field gets case predicates.  So: the "none" skip inside loadBl after `type = e->type;` (the load comes before strnicmp
clobbers memory: `nib`), or with the switch on `e->type` itself and narrow `type` locals (`sw_<type>`).  Crossed with
gen_bd510's offs.  Runs on src as of 53c5fc43.  `python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd520.py`."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun
from gen_bd510 import LB_HEAD, lbf, off, OFFS

FOCUS = ['_loadBlFiles']

SW = LB_HEAD + '\n\ttype = e->type;\n\tswitch (type) {\n'
CALL = '\t\tif (strnicmp(e->name, "none", 4) || e->crc)\n\t\t\tloadBl(e, i, &r);\n'


def nib(t, form):
    skip = {
        'and': '\tif (!strnicmp(e->name, "none", 4) && !e->crc)\n\t\treturn;\n',
        'nest': '\tif (!strnicmp(e->name, "none", 4)) {\n\t\tif (!e->crc)\n\t\t\treturn;\n\t}\n',
    }[form]
    t = bdrun.sub(t, SW, LB_HEAD + '\n\ttype = e->type;\n' + skip + '\tswitch (type) {\n', 1)
    return lbf(t, CALL, '\t\tloadBl(e, i, &r);\n')


def swn(t, ty):
    return bdrun.sub(t, SW, LB_HEAD.replace('\tint type;', '\t%s type;' % ty) + '\n\ttype = e->type;\n\tswitch (e->type) {\n', 1)


VARIANTS = {
    'src': lambda t: t,
    'nib_and': lambda t: nib(t, 'and'),
    'nib_nest': lambda t: nib(t, 'nest'),
}
for ty in ('uint8_t', 'uint16_t', 'unsigned', 'uint32_t'):
    VARIANTS['sw_' + ty] = lambda t, ty=ty: swn(t, ty)


def CASES(base):
    return [('%s|%s' % (v, k), lambda b, f=f, k=k: off(f(b), k)) for v, f in VARIANTS.items() for k in OFFS]
