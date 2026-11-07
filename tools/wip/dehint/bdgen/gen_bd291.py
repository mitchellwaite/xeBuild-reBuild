"""Attempt 18, exp_pr (and t5le): stack predictors on the `*pr`-true edge with redundant tests that thread away.

`*pr` is a known constant (0 or -1) on every path into the `xb.type <= BUILD_DEVGL16` tail once vrp1/dom2 have
threaded it, so any test of `*pr` there leaves no code; but each test block gets its own heuristic at
profile_estimate, and the thread's path_out is the product along the path.  gen_bd263 tried one test at a time
(`== -1` 37.8%, `< 0`); here two or three are chained (nested ifs or `&&`), and the `*pr` value is read once into a
local or re-read.  Axes: the test chain, the t5le label kept or not.  No `*pr` expect.  Runs on src as of 8b56de61."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

OLD = '''		if (xb.type <= BUILD_DEVGL16) {
		t5le: __attribute__((hot));
			if (__builtin_expect(*pr != 0, 0))
				goto fail;
			break;
		}
'''
T = {
    'ne0': ['*pr != 0'],
    'eqm1': ['*pr == (uint32_t)-1'],
    'neg': ['(int)*pr < 0'],
    'ne0.eqm1': ['*pr != 0', '*pr == (uint32_t)-1'],
    'neg.eqm1': ['(int)*pr < 0', '*pr == (uint32_t)-1'],
    'eqm1.neg': ['*pr == (uint32_t)-1', '(int)*pr < 0'],
    'neg.ne0': ['(int)*pr < 0', '*pr != 0'],
    'eqm1.ne0': ['*pr == (uint32_t)-1', '*pr != 0'],
    'neg.eqm1.ne0': ['(int)*pr < 0', '*pr == (uint32_t)-1', '*pr != 0'],
    'eqm1.neg.ne0': ['*pr == (uint32_t)-1', '(int)*pr < 0', '*pr != 0'],
}


def mk(b, tk, form, lab):
    ts = T[tk]
    head = '\t\tif (xb.type <= BUILD_DEVGL16) {\n' + ('\t\tt5le: __attribute__((hot));\n' if lab else '')
    if form == 'and':
        body = '\t\t\tif (' + ' && '.join(ts) + ')\n\t\t\t\tgoto fail;\n\t\t\tbreak;\n'
    else:
        body = ''
        ind = '\t\t\t'
        for t in ts:
            body += ind + 'if (' + t + ')\n'
            ind += '\t'
        body = body[:-1] + '\n' if False else body
        body += ind + 'goto fail;\n\t\t\tbreak;\n'
    new = head + body + '\t\t}\n'
    return bdrun.sub(b, OLD, new, 1)


def CASES(base):
    out = []
    for tk, form, lab in itertools.product(T, ['and', 'nest'], [0, 1]):
        if len(T[tk]) == 1 and form == 'nest':
            continue
        out.append(('%s %s lab%d' % (tk, form, lab), lambda b, c=(tk, form, lab): mk(b, *c)))
    return out


FOCUS = ['_loadBlFiles']
