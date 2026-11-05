"""gen_bd140's axes again on build/bd/a5/lb6.c (goto chk for CG, no expect on 10), with and without the size label."""
import itertools, importlib.util, os
spec = importlib.util.spec_from_file_location('g140', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_bd140.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

BASE = 'build/bd/a5/lb6.c'


def CASES(base):
    a = base.index('if (type == 5 || type == 17 || type == 11) {')
    b = base.index('case 6:', a)
    b = base.rindex('\n', 0, b) + 1
    out = []
    for s, ty, fl, nest, bad in itertools.product(g.SIGS, g.TY, g.FL, ('in', 'out'), (0, 1)):
        body = g.TY[ty].replace('@@', g.SIGS[s])
        if nest == 'in':
            new = body + g.FL[fl] + '}\nbreak;\n'
        else:
            if fl in ('le', 'lee') or ty == 'sw':
                continue
            new = body + '}\n' + g.FL[fl].replace('if (', 'if (!*pr && ', 1) + 'break;\n'
        t = base[:a] + new + base[b:]
        if bad:
            t = t.replace('log_printf(1, "\\n\\n***** ERROR: patch size', 'badsize: __attribute__((hot));\nlog_printf(1, "\\n\\n***** ERROR: patch size', 1)
        out.append(('%s %s %s %s bad%d' % (s, ty, fl, nest, bad), t))
    return out
