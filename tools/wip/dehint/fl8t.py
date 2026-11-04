"""fl8t.py <tag> [n]: dom3's popped names in order, each with its definition before ivopts (124t.sink), and whose loop.  For comparing free stacks
of two flpass dumps (build/filelist_ini/dump/<tag>)."""
import glob, os, re, sys
import fllib as L

tag = sys.argv[1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 45


def sect(pat):
    f = glob.glob(os.path.join(L.BD, 'dump', tag, '-.*t.' + pat))[0]
    t = open(f, errors='replace').read()
    return [q for q in re.split(r'(?m)^(?=;; Function )', t) if q.startswith(';; Function parseIni ')][0]


def defs(q):
    d = {}
    for ln in q.splitlines():
        m = re.match(r'\s*(?:# )?([\w.]*_(\d+))(?:\(D\))? = (.*)', ln)
        if m:
            d[int(m.group(2))] = m.group(1) + ' = ' + m.group(3)
    return d


split = defs(sect('split-paths'))
d3 = sect('dom3')
new = []
for ln in d3.splitlines():
    m = re.match(r'\s*(?:# )?([\w.]*_(\d+))(?:\(D\))? = (.*)', ln)
    if m and int(m.group(2)) not in split:
        new.append((int(m.group(2)), m.group(0).strip()))
snk = defs(sect('sink'))
ivo = defs(sect('ivopts'))
for n, txt in new[:N]:
    print('%-40s was %s' % (txt[:40], snk.get(n, '-')[:50]))
gone = sorted(set(snk) - set(ivo))
print('gone at ivopts', len(gone))
print('ivopts new', [k for k in ivo if k not in snk][:40])
