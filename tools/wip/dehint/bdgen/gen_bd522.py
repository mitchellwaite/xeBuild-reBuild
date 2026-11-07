"""Attempt 40: attempt 9's reconstruction C (gen_bd202: the switch in `static int loadBl(e, i)`, r returned) with the
none test inside the helper scored 9999 because loadBl wasn't inlined: strnicmp clobbers memory before the e->type
load, so ipa-inline-analysis gets no case predicates and the early min_size check refuses the edge.  Here the type is
loaded first (`int type = e->type;` above the none test), so the switch is on an unmodified parameter load again.
Rows `in` (rescued) against gen_bd202's `r0` / `else` call forms.  No hints, as gen_bd202.  Runs on src as of 53c5fc43.
`python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd522.py`."""
import importlib.util, itertools, os
d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g202', os.path.join(d, 'gen_bd202.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

FOCUS = ['_loadBlFiles']
OLD = '''	int type;

	if (!strnicmp(e->name, "none", 4) && !e->crc)
		return 0;
	type = e->type;
'''
NEW = '''	int type = e->type;

	if (!strnicmp(e->name, "none", 4) && !e->crc)
		return 0;
'''


def CASES(base):
    out = []
    for fb, order, sig, rtype, form in itertools.product(['con2', 'and'], ['5_17_11', '17_5_11'], ['N', 'L', 'P'],
                                                         ['int', 'uint32_t'], ['r0', 'in']):
        kw = dict(fb=fb, order=order, sig=sig, tail='and', guard='nest', size='else')

        def f(b, kw=kw, rtype=rtype, form=form):
            t = g.helper(b, 'r0', rtype, form == 'in', **kw)
            return t.replace(OLD, NEW, 1) if form == 'in' else t
        out.append(('%s %s %s %s %s' % (fb, order, sig, form, rtype), f))
    return out
