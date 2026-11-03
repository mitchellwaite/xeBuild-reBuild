"""Index expressions scev can't follow but a later pass could remove (diagnostic for the imul)."""
import itertools
from importlib import util
import os

_s = util.spec_from_file_location('g2', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_ca2.py'))
g2 = util.module_from_spec(_s)
_s.loader.exec_module(g2)

KS = {
    'u16': ('int i; uint16_t k;', 'k', 'k = i;'),
    's16': ('int i; short k;', 'k', 'k = i;'),
    'u8': ('int i; uint8_t k;', 'k', 'k = i;'),
    'and': ('int i; int k;', 'k', 'k = i & 0xff;'),
    'and2': ('int i; int k;', 'k', 'k = i & 0x7fffffff;'),
    'mod': ('int i; int k;', 'k', 'k = i % 256;'),
    'min': ('int i; int k;', 'k', 'k = i < 256 ? i : 255;'),
    'min2': ('int i; int k;', 'k', 'k = i > 255 ? 255 : i;'),
    'max': ('int i; int k;', 'k', 'k = i < 0 ? 0 : i;'),
    'abs': ('int i; int k;', 'k', 'k = abs(i);'),
    'abs2': ('int i; int k;', 'k', 'k = i < 0 ? -i : i;'),
    'shr': ('int i; int k;', 'k', 'k = (uint32_t)i << 1 >> 1;'),
    'sxt': ('int i; int k;', 'k', 'k = (short)i;'),
    'dbl': ('int i; int k;', 'k', 'k = (int)(double)i;'),
    'sel': ('int i; int k;', 'k', 'if (i >= 0) k = i; else k = 0;'),
    'iu8': ('uint8_t i;', 'i', ''),
    'iu16': ('uint16_t i;', 'i', ''),
    'is16': ('short i;', 'i', ''),
    'll': ('long long i;', 'i', ''),
    'ull': ('uint64_t i;', 'i', ''),
    'u32': ('uint32_t i;', 'i', ''),
}


def variants():
    g2.IDX.clear()
    g2.IDX.update(KS)
    for acc, idx, lp in itertools.product(['idx', 'arith', 'ptr'], KS, ['do', 'for', 'inf']):
        b = g2.body(acc, idx).replace('%%', '%')
        src = g2.PREP + g2.HEAD % {'decl': KS[idx][0], 'loop': g2.LOOPS[lp] % b.replace('%', '%%')}
        yield '%s|%s|%s' % (acc, idx, lp), src
