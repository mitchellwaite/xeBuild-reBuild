"""python tools/wip/dehint/iw5d.py <file.c> [-np] [fn ...]: diff against reference.o with jump/call targets and .rdata literal offsets blanked,
so only real instruction differences show.  Prints core-line counts per function, then the diffs (of the named functions, or all with few lines)."""
import difflib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib


def norm(ls):
    out = []
    for l in iwlib.strip_addr(ls):
        l = re.sub(r'^((?:j[a-z]+|call)\s+)[0-9a-f]+$', r'\1T', l)
        out.append(l)
    return out


def core(o):
    """{fn: lines} ignoring jump targets"""
    r = iwlib.ref()
    fns, order = iwlib.disasm(o)
    per = {}
    for n in r['order']:
        if n not in fns:
            per[n] = 9999
            continue
        a, b = norm(r['fns'][n]), norm(fns[n])
        if a != b:
            per[n] = sum(1 for l in difflib.ndiff(a, b) if l[0] in '+-')
    return per, fns


if __name__ == '__main__':
    a = sys.argv[1:]
    path = a.pop(0)
    flags = ['--param', 'builtin-expect-probability=50']
    if '-np' in a:
        a.remove('-np')
        flags = []
    text = open(path, newline='').read().replace('\r\n', '\n')
    ok, o, d = iwlib.compile_src(text, flags)
    if not ok:
        print('COMPILE ERROR', o)
        sys.exit(1)
    idn, tot, per, notes = iwlib.report(o)
    print('IDENTICAL' if idn else '%d %s %s' % (tot, per, ' '.join(notes)))
    if not idn:
        c, fns = core(o)
        print('core', sum(c.values()), c)
        r = iwlib.ref()
        for n in c:
            if a and n not in a:
                continue
            if not a and c[n] > 200:
                continue
            print('=====', n)
            for l in difflib.unified_diff(norm(r['fns'][n]), norm(fns[n]), lineterm='', n=1):
                if not l.startswith(('---', '+++')):
                    print(l)
    iwlib.cleanup(d)
