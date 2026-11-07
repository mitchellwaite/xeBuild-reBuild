"""Attempt 33: pin_d by the case 27 smcConfig fallback's own statements (never swept: gen_bd40/113/191/271/317/422 changed
the tail, the address spelling, the load chain, helpers, scope and case order).  The fallback's four moves in every
order (src has data, NULL, size, 0, unlike cases 2/3/4's data, size, NULL, 0), the take-over block nested
(`if (xb.smcConfig.data) {..}`) or src's `if (!..) break;`, and `*pr = 0` first or last; pin_d off and on.
Runs on src as of 5a0bc459."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdhints, bdrun

FOCUS = ['_loadBlFiles']

OLD = '''			if (!xb.smcConfig.data)
				break;
			log_printf(1, "reading %s%s failed, using %s from nand dump\\n", xb.baseDir, e->name, e->name);
			if (xb.files[xb.nFlashFiles].data)
				free(xb.files[xb.nFlashFiles].data);
			xb.files[xb.nFlashFiles].data = xb.smcConfig.data;
			xb.smcConfig.data = NULL;
			xb.files[xb.nFlashFiles].size = xb.smcConfig.size;
			xb.smcConfig.size = 0;
			*pr = 0;
		}
'''
MOVES = ['xb.files[xb.nFlashFiles].data = xb.smcConfig.data;', 'xb.smcConfig.data = NULL;',
         'xb.files[xb.nFlashFiles].size = xb.smcConfig.size;', 'xb.smcConfig.size = 0;']


def form(order, nest, prfirst):
    mv = [MOVES[i] for i in order]
    # a move that reads a source after it was cleared changes behaviour: keep only valid orders
    if order.index(1) < order.index(0) or order.index(3) < order.index(2):
        return None
    ind = '\t\t\t\t' if nest else '\t\t\t'
    body = [ind + 'log_printf(1, "reading %s%s failed, using %s from nand dump\\n", xb.baseDir, e->name, e->name);',
            ind + 'if (xb.files[xb.nFlashFiles].data)', ind + '\tfree(xb.files[xb.nFlashFiles].data);']
    if prfirst:
        body.append(ind + '*pr = 0;')
    body += [ind + m for m in mv]
    if not prfirst:
        body.append(ind + '*pr = 0;')
    if nest:
        return '\t\t\tif (xb.smcConfig.data) {\n' + '\n'.join(body) + '\n\t\t\t}\n\t\t}\n'
    return '\t\t\tif (!xb.smcConfig.data)\n\t\t\t\tbreak;\n' + '\n'.join(body) + '\n\t\t}\n'


def CASES(base):
    out = []
    for order in itertools.permutations(range(4)):
        for nest in (0, 1):
            for prf in (0, 1):
                nb = form(order, nest, prf)
                if nb is None:
                    continue
                for pin in ('off', 'on'):
                    lab = '%s %s %s pin_%s' % (''.join(map(str, order)), 'nest' if nest else 'brk', 'pr1' if prf else 'pr9', pin)
                    out.append((lab, lambda b, nb=nb, pin=pin: (bdhints.off(bdrun.sub(b, OLD, nb), 'pin_d') if pin == 'off'
                                                               else bdrun.sub(b, OLD, nb))))
    return out
