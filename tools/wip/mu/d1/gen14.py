"""gen14.py: success path of updateNand moved to a static helper.  Then bb4 is one call right before the return block, so `if (!ret)` has early return on both edges: 50/50, and 128 can tie 105."""
import itertools
import re

import axes as a
import sw


def split(s, proto='static void flashConsole(char *dumpDir, int ret, int *pret)', call='flashConsole(dumpDir, ret, pret);'):
    i0 = s.index('\t\t\tnetUnmount("usv");')
    i1 = s.index('\t\t} else {\n\t\t\tlog_printf(0, "\\n\\n***** FATAL UPDATE ERROR: %i unable')
    body = s[i0:i1]
    body = '\n'.join(l[2:] if l.startswith('\t\t') else l for l in body.split('\n'))
    hat = 'static void updateNand(char *dumpDir, int *pret)\n'
    s = s[:i0] + '\t\t\t' + call + '\n' + s[i1:]
    s = s.replace('\tint ret, r;\n', '\tint ret;\n')
    return s.replace(hat, proto + '\n{\n\tint r;\n\n' + body + '}\n\n' + hat)


if __name__ == "__main__":
    vs = []
    for (rk, rv), (ek, ev), (ik, iv) in itertools.product(a.REB.items(), a.ERRS.items(), a.IPS.items()):
        s = a.build(a.HEAD, rv, ev, iv)
        vs.append(('%s_%s_%s' % (rk, ek, ik), split(s)))
    print(len(vs))
    sw.run(vs, '-O3', save='gen14', top=25)
