"""Flag forms and common-tail forms x readFileTo spellings that still match (rfsig.py)."""
import importlib.util, itertools, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


g14 = load('gen_rf14')
g15 = load('gen_rf15')
J = json.load(open(os.path.join(ROOT, 'build', 'rf', 'rfsig.json')))
SIGS = [(t, x) for t, x in J['sigs'] if t.split('|')[1] == 'size_t' and t.split('|')[4] == 'a']
OLD = J['old']


def variants():
    for (st, text) in SIGS:
        rep = [] if text == OLD else None
        # rfsweep replaces text in the part of the file before readFileIn
        rep = [(OLD, text)]
        for (fn, (init, fl)), (tn, t) in itertools.product(g14.FLAG.items(), g14.TAIL.items()):
            if fn in ('err', 'errb', 'bn'):
                continue
            decl = '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\tint %s;\n\n' % init
            eo, ec = g14.ENTRY['nest']
            s = g14.HEAD + decl + eo + g14.PREP + fl.replace('LOG', g14.LOG).replace('RD', g14.RD) + t + ec + '\treturn buf;\n}\n'
            yield '|'.join(['fl', fn, tn, st]), s, [], rep
        for (bn, b), (tn, t) in itertools.product(g15.BODY.items(), g15.TAIL.items()):
            eo, ec = g15.ENTRY['nest']
            s = g15.HEAD + '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\n' + eo + g15.PREP + b.replace('LOG', g15.LOG).replace('RD', g15.RD).replace('OK', g15.OK) + t + ec + '\treturn buf;\n}\n'
            yield '|'.join(['ct', bn, tn, st]), s, [], rep
