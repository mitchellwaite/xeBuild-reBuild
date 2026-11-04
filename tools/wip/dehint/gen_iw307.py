# attempt 24, pin_t: gen_iw305's U table below and above the rescale point, to separate its name effects from the rescale's (2391 * (n + 1) passes 10000 at n = 4).
# `IWB=build/iw/a24/np.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw307.py -n 12 -t 4`
import importlib.util, os
sp = importlib.util.spec_from_file_location('g305', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_iw305.py')); g = importlib.util.module_from_spec(sp); sp.loader.exec_module(g)
AXES = [[('U%d' % n, [(g.S8, g.tab('s[8]', 'len >> 8', n, 'uint32_t', '						') + g.S8[g.S8.index('						s[7]'):])]) for n in (2, 3, 4)]]
