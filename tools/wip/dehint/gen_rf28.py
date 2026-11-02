"""Compare operator axis on the scoped shapes: `read < size` / `read >= size` have no opcode heuristic (50%, as the hinted source's `if (ok)`), `==` gets 28%."""
import importlib.util, itertools, os, re


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R = 'readFileTo(path, buf, size)'
EQ = {'ge': R + ' >= size', 'le': 'size <= ' + R, 'ngt': '!(' + R + ' < size)'}
NE = {'ge': R + ' < size', 'le': 'size > ' + R, 'ngt': R + ' < size'}
G = {g: load(g) for g in ('gen_rf22', 'gen_rf23', 'gen_rf24', 'gen_rf25')}


def variants():
    seen = set()
    for g, m in G.items():
        for v in m.variants():
            tag, s = v[0], v[1]
            if R not in s:
                continue
            for k in EQ:
                t = s.replace(R + ' == size', EQ[k]).replace(R + ' != size', NE[k])
                if t == s or t in seen:
                    continue
                seen.add(t)
                yield '|'.join([k, g[-2:], tag]), t
