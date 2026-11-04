"""python tools/wip/dehint/iw13an.py <seconds> <seed> <base.c> [--workers N]: iw8an's anneal over imgAdd's and writeFsTable's forms, with writeFsTable counted in the score (it isn't decoupled on the bitfield family). Log build/iw/a8/an8_<seed>.log, hits an8_<seed>_<n>.c."""
import os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'iw8an.py')
src = open(p).read().replace("per.pop('_writeFsTable', None)", "pass")
__file__ = p
exec(compile(src, p, 'exec'))
