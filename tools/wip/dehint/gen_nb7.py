"""Borderline review, net: with the select arm's `size = 0; if (!size) return NULL;` (gen_nb5),
the recv arm's in-loop test and the post-loop status test, spelled each way."""
from nbsweep import BASE
import gen_nb4 as G

TESTS = {'ne1': 'status != 1', 'not': '!status', 'eq0': 'status == 0', 'lt1': 'status < 1'}


def build(lt, pt):
    body = (G.SEL + '\t\t\t\tsize = 0;\n\t\t\t}\n\t\t\tif (!size)\n\t\t\t\treturn NULL;\n' +
            G.RECV + '\t\t\t\tstatus = 0;\n\t\t\t}\n\t\t\tif (' + TESTS[lt] + ')\n\t\t\t\tbreak;\n')
    lp = G.loop('got < size', body).replace(G.POST, '\t\tif (' + TESTS[pt] + ')\n\t\t\treturn NULL;\n')
    return BASE[:G.A] + lp + BASE[G.B:]


def variants():
    for lt in TESTS:
        for pt in TESTS:
            yield '%s|%s' % (lt, pt), build(lt, pt)
