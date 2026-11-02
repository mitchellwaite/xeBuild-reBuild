"""Signed `size` (int/long) on the scoped shapes."""
import importlib.util, itertools, os, re


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R = 'readFileTo(path, buf, size)'
G = {g: load(g) for g in ('gen_rf22', 'gen_rf23', 'gen_rf24', 'gen_rf25')}
FORMS = {'eq': (R + ' == size', R + ' != size'),
         'ge': (R + ' >= size', R + ' < size'),
         'sge': ('(int)' + R + ' >= size', '(int)' + R + ' < size'),
         'seq': ('(int)' + R + ' == size', '(int)' + R + ' != size')}


KEEP = {'a|mid|void', 'b|mid|void', 'c|mid|void', 'h2|1|ob|mid', 'h4|1|ob|mid', 'h5|1|ob|mid', 'h1n|1|ob|mid', 'bf|sep', 'err|sep', 'nf|sepn', 'i1|sep', 'asb|Aob', 'as|Dob', 'bf|Aob', 'nf|Aob', 'bf|Dob', 'nf|Dob', 'c|ob|mid', 'e|ob|mid', 'S|ob|mid', 'A|ob|mid', 'D|ob|mid'}


def variants():
    seen = set()
    for g, m in G.items():
        for v in m.variants():
            tag, s = v[0], v[1]
            if 'size_t size, alloc;' not in s:
                continue
            if tag not in KEEP:
                continue
            for ty, aty in itertools.product(['int', 'long'], ['size_t', 'int']):
                t0 = s.replace('size_t size, alloc;', '%s size;\n\t%s alloc;' % (ty, aty))
                for k, (a, b) in FORMS.items():
                    t = t0.replace(R + ' == size', a).replace(R + ' != size', b)
                    if t in seen:
                        continue
                    seen.add(t)
                    yield '|'.join([ty, aty, k, g[-2:], tag]), t
