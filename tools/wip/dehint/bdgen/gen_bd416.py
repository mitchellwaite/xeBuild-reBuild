"""Attempt 30: the no-key-first signature form (`if (!xb.pub1bl) nokey; else if (!verify) {failed} else if (type) passed;`)
and the positive forms on src itself (every hint kept), then each loadBl hint off alone on it: is it an equal base, and
does any hint get cheaper there?  Axes: sig (src, nk, nkp), base (src, and9+c2), hint off (none or one).
Runs on src as of 6083630d."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun, bdhints
import a30lib
import gen_bd410 as g0

SRC = '''			if (xb.pub1bl) {
				if (!cbVerifySig(e->data, xb.pub1bl)) {
					log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
					*pr = -1;
				/* Borderline, for review: type is 5, 11 or 17 here, so this test
				   is always true; a plain else costs 54 lines */
				} else if (type)
					log_printf(1, "loaded %s, signature check passed!\\n", e->name);
			} else
				log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);
'''
NK = '''			if (!xb.pub1bl)
				log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);
			else if (!cbVerifySig(e->data, xb.pub1bl)) {
				log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
				*pr = -1;
			} else if (type)
				log_printf(1, "loaded %s, signature check passed!\\n", e->name);
'''
NKN = NK.replace('\t\t\t} else if (type)\n', '\t\t\t} else\n')
SIGS = {'src': SRC, 'nk': NK, 'nkn': NKN}
OFFS = ['', 'exp_t10', 'exp_pr', 'lab_t5le', 'vol_fail', 'cp', 'etype']


def mk(b, sig, base, off):
    if base == 'c2':
        b = g0.and9c2(b)
    b = bdrun.sub(b, SRC, SIGS[sig], 1)
    if off == 'etype':
        if sig == 'src':
            b = a30lib.off7(b, keep=('exp_t10', 'exp_pr', 'lab_t5le', 'vol_fail', 'cp'))
        elif sig == 'nk':
            b = bdrun.sub(b, '\t\t\t} else if (type)\n', '\t\t\t} else\n', 1)
        else:
            return None
    elif off == 'cp':
        b = bdrun.sub(b, a30lib.CPBLK, '', 1)
    elif off:
        b = bdhints.off(b, off)
    return b


def CASES(base):
    return [(' '.join(k) or 'none', lambda b, k=k: mk(b, *k)) for k in itertools.product(SIGS, ['src', 'c2'], OFFS)]


FOCUS = ['_loadBlFiles']
