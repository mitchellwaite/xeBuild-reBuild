"""keysend.py <file of forms>: try daeEncrypt variants, each given as (old, new) text edits on the
attempt 1 daeEncrypt with its dead test taken out.  Set KEYSBASE=drafts/keys_final.c: the edits expect that
source, not one already in the exit-arm shape.

A forms file is python: FORMS = {name: {'tail': text} or {'edits': [(old, new), ...]}}.
LW in a tail stands for the warning call.  Prints each form's score at plain -O3, best last;
MATCH only for a whole-object byte match.  keysend_forms.py holds attempt 2's forms."""
import re, runpy, sys
from multiprocessing.pool import ThreadPool
import keyslib as K
from keysfn import replace_fn

LW = r'log_printf(0, "\n******* WARNING: dae data appears to be crypted with a different key or damaged! Skipping encryption.\n");'
OLDTAIL = 'if (n != 2)\n\t\t' + LW + '\n\tif (orig)\n\t\tfree(orig);\n'
SRC = K.base()
m = re.search(r'^void daeEncrypt\(.*\)\n\{', SRC, re.M)
BODY = SRC[m.start():SRC.index('\n}\n', m.end()) + 3]
assert OLDTAIL in BODY


def build(f):
    b = BODY
    if 'tail' in f:
        b = b.replace(OLDTAIL, f['tail'].replace('LW', LW) + '\n')
    else:
        b = b.replace(OLDTAIL, 'if (n != 2)\n\t\t' + LW + '\n\tfree(orig);\n')
    for old, new in f.get('edits', []):
        assert old in b, old
        b = b.replace(old, new)
    return replace_fn(SRC, 'daeEncrypt', b + '\n')


def run(forms, width=4):
    names = list(forms)
    slots = [names[i::width] for i in range(width)]

    def work(a):
        i, sl = a
        out = []
        for n in sl:
            s = build(forms[n])
            o = K.compile(s, ['-O3'], 'e%d' % i)
            out.append((n, K.same(o), K.fndiff(o) if o else {'fail': 9999}))
            if out[-1][1]:
                open(K.os.path.join(K.R, 'build', 'keys', 'a2', 'match_%s.c' % n), 'w', newline='\n').write(s)
        return out
    with ThreadPool(width) as p:
        res = sum(p.map(work, list(enumerate(slots))), [])
    res.sort(key=lambda r: -sum(r[2].values()))
    for r in res:
        print('MATCH' if r[1] else '     ', r[0], sum(r[2].values()), r[2])


if __name__ == '__main__':
    run(runpy.run_path(sys.argv[1])['FORMS'])
