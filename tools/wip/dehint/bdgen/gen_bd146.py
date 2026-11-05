"""lb6 grid: signature form x subsets of the old hints x tail form, looking for any byte-identical state with fewer hints than src."""
import itertools, importlib.util, os, re
d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g144', os.path.join(d, 'gen_bd144.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
spec = importlib.util.spec_from_file_location('g140', os.path.join(d, 'gen_bd140.py'))
s0 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s0)

BASE = 'build/bd/a5/lb6.c'


def ws(old):
    return r'[ \t]*' + r'\n[ \t]*'.join(re.escape(l) for l in old.split('\n'))


def nobar(t):
    return t.replace('\t__asm__ __volatile__("");\n', '')


H = dict(g.H)
H['nobar'] = nobar
BODY = {
    'nest': None,
    'brk': 1,
}


def CASES(base):
    a = base.index('if (!xb.pub1bl)', base.index('chk:'))
    b = base.index('if (xb.type <= BUILD_DEVGL16)\nbreak;', a)
    # the signature text inside the type test
    out = []
    names = ['t10', 'bad', 'cp', 'nopin', 'nobar']
    for sg in ('notel', 'cur'):
        for n in range(len(names) + 1):
            for s in itertools.combinations(names, n):
                for k, f in g.TAIL.items():
                    for bd in BODY:
                        t = base[:a] + s0.SIGS[sg] + '}\n' + base[b:]
                        if bd == 'brk':
                            t = t.replace('*pr = checkBl(e->data, e->size, type, e->crc);\nif (!*pr) {\nif (type == 5', '*pr = checkBl(e->data, e->size, type, e->crc);\nif (*pr)\nbreak;\nif (type == 5', 1)
                            t = t.replace('if (type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n}\nbreak;\n', 'if (type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\nbreak;\n', 1)
                        for x in s:
                            t = H[x](t)
                        if f:
                            t = f(t)
                        out.append((','.join((sg, bd) + s + (k,)), t))
    return out
