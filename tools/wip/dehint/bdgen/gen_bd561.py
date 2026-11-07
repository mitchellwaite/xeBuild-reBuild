"""Attempt 45: on the loop-form near miss n1 (a45lib.loop fb=con2 sz=and3, etype + cp + lab_t5le off; 14 loose / 34 strict
at p99, only case 24's r = 1 block after the first arm placed late), the structure axes again plus case 24's forms.
Run at p99: `BDEXTRA='--param builtin-expect-probability=99' python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd561.py -n 400`."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun
import a45lib
from a45lib import loop

FOCUS = None

A1 = '''if (loadBaseFile(e->name, e))
							r = defaultBl60(e);
						else if (e->size != 0x60)
							r = defaultBl60(e);
					}
					if (xb.type == BUILD_DEVGL'''
A1OR = '''if (loadBaseFile(e->name, e) || e->size != 0x60)
							r = defaultBl60(e);
					}
					if (xb.type == BUILD_DEVGL'''
A2 = '''r = 0;
						if (loadBaseFile(e->name, e))
							r = defaultBl60(e);
						else if (e->size != 0x60)
							r = defaultBl60(e);'''
A2OR = '''r = 0;
						if (loadBaseFile(e->name, e) || e->size != 0x60)
							r = defaultBl60(e);'''


def c24(sw, v):
    if v in ('or1', 'orb'):
        sw = bdrun.sub(sw, A1.replace('\t\t\t\t\t', '\t\t'), A1OR.replace('\t\t\t\t\t', '\t\t'), 1)
    if v in ('or2', 'orb'):
        sw = bdrun.sub(sw, A2.replace('\t\t\t\t\t', '\t\t'), A2OR.replace('\t\t\t\t\t', '\t\t'), 1)
    return sw


a45lib.EXTRA['c24'] = c24
BASEOFF = ('etype', 'cp', 'lab_t5le')


def CASES(base):
    out = []
    for fail, tail, c6, rdecl, c24v in itertools.product(['c2', 'c23', 'each'], ['src', 'plain', 'and'], [False, True],
                                                         ['body', 'top'], ['src', 'or1', 'or2', 'orb']):
        offs = [BASEOFF]
        if tail == 'src':
            offs.append(BASEOFF + ('exp_pr',))
        if fail != 'each':
            offs.append(BASEOFF + ('vol_fail',))
        for off in offs:
            off = tuple(o for o in off if not (o == 'lab_t5le' and tail != 'src'))
            lab = '%s %s %s %s %s|%s' % (fail, tail, 'c6' if c6 else '-', rdecl, c24v, '+'.join(off[3:] if tail == 'src' else off[2:]) or '-')
            out.append((lab, lambda t, kw=dict(fb='con2', sz='and3', fail=fail, tail=tail, c6=c6, rdecl=rdecl, c24=c24v, off=off): loop(t, **kw)))
    return out
