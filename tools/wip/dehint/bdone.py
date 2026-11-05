"""One hint off, one edit: python tools/wip/dehint/bdone.py <gen.py> [-n TOP] [-o a,b]

A generator module defines CASES: a list of (off, label, fn) where off is a comma list of bdtricks
names, label names the edit and fn(text) gives the edited source (None to skip; '' as label with
fn None scores the removal alone).  BASE (optional) is the source to start from.  Prints, per
`off`, its score alone and every edit that beats it, best first.  -o keeps only those `off`s.

Helpers for generators:
  fnspan(text, head)      (start, end) of the function whose definition starts with head
  infn(head, old, new, n=None)  edit inside that function: replace the nth (default all) old
  retype(head, var, new)  give local or parameter var the type new
  vars_of(text, head)     [(name, type)] of integer parameters and locals of the function"""
import importlib.util, os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, bdtricks


def fnspan(text, head):
    i = text.find('\n' + head)
    while i >= 0 and not text[text.find(')', i) + 1:].startswith('\n{'):  # a prototype
        i = text.find('\n' + head, i + 1)
    if i < 0:
        raise ValueError('no function ' + head)
    j = text.find('\n}\n', i)
    return i + 1, j + 3


def infn(head, old, new, n=None):
    def f(text):
        a, b = fnspan(text, head)
        s = text[a:b]
        if old not in s:
            return None
        if n is None:
            s = s.replace(old, new)
        else:
            parts = s.split(old)
            if n + 1 >= len(parts):
                return None
            s = old.join(parts[:n + 1]) + new + old.join(parts[n + 1:])
        return text[:a] + s + text[b:]
    return f


DECL = re.compile(r'^(\t+)((?:const )?(?:unsigned int|int|uint32_t|uint16_t|uint8_t|size_t|long|char|BOOL)) ([^;()]+);$', re.M)
INTS = ('int', 'uint32_t', 'size_t', 'long', 'unsigned int', 'uint16_t', 'BOOL')


def split_decl(body):
    out, depth, cur = [], 0, ''
    for c in body:
        if c in '([':
            depth += 1
        if c in ')]':
            depth -= 1
        if c == ',' and not depth:
            out.append(cur.strip())
            cur = ''
        else:
            cur += c
    out.append(cur.strip())
    return out


def vars_of(text, head):
    a, b = fnspan(text, head)
    s = text[a:b]
    res = []
    hd = s[:s.index(')')]
    for p in hd[hd.index('(') + 1:].split(','):
        m = re.match(r'\s*((?:unsigned )?\w+) (\w+)$', p)
        if m and m.group(1) in INTS:
            res.append((m.group(2), m.group(1)))
    for m in DECL.finditer(s):
        for d in split_decl(m.group(3)):
            k = re.match(r'(\w+)(\s*=.*)?$', d)
            if k and m.group(2) in INTS:
                res.append((k.group(1), m.group(2)))
    return res


def retype(head, var, new):
    def f(text):
        a, b = fnspan(text, head)
        s = text[a:b]
        par = s.index(')')
        hd = s[:par + 1]
        h2 = re.sub(r'(\(|, )((?:unsigned )?\w+) %s(,|\))' % var, lambda m: m.group(1) + new + ' ' + var + m.group(3), hd)
        if h2 != hd:
            return text[:a] + h2 + s[par + 1:] + text[b:]
        for m in DECL.finditer(s):
            ds = split_decl(m.group(3))
            for d in ds:
                k = re.match(r'(\w+)(\s*=.*)?$', d)
                if k and k.group(1) == var:
                    rest = [x for x in ds if x != d]
                    line = m.group(1) + new + ' ' + d + ';'
                    if rest:
                        line = m.group(1) + m.group(2) + ' ' + ', '.join(rest) + ';\n' + line
                    return text[:a] + s[:m.start()] + line + s[m.end():] + text[b:]
        return None
    return f


def load(p):
    s = importlib.util.spec_from_file_location('gen', p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def main():
    a = sys.argv[1:]
    top = 8
    only = None
    if '-n' in a:
        i = a.index('-n')
        top = int(a[i + 1])
        del a[i:i + 2]
    if '-o' in a:
        i = a.index('-o')
        only = a[i + 1].split(';')
        del a[i:i + 2]
    m = load(a[0])
    base = bdlib.read_src(os.path.join(bdlib.R, getattr(m, 'BASE', 'src/build.c')))
    cases = m.CASES(base) if callable(m.CASES) else m.CASES
    if only:
        cases = [c for c in cases if c[0] in only]
    print(len(cases), 'cases', flush=True)

    def one(c):
        off, label, fn = c
        t = bdtricks.apply(base, [x for x in off.split(',') if x and x in bdtricks.T])[0]
        if fn:
            t = fn(t)
            if t is None:
                return off, label, None
        return off, label, bdlib.score_text(t, bdtricks.flags())

    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(one, cases))
    alone = {}

    def single(off):
        t = bdtricks.apply(base, [x for x in off.split(',') if x and x in bdtricks.T])[0]
        return off, bdlib.score_text(t, bdtricks.flags())
    offs = sorted(set(r[0] for r in res))
    with ThreadPoolExecutor(4) as ex:
        alone = dict(ex.map(single, offs))
    for off in offs:
        k0 = alone[off].get('total', 10**9)
        print('== %s alone %s' % (off or '(none)', bdlib.fmt(alone[off])[:110]))
        rs = [r for r in res if r[0] == off and r[2] and 'total' in r[2]]
        rs.sort(key=lambda r: r[2]['total'])
        shown = 0
        for r in rs:
            if r[2].get("identical") or (r[2]["total"] <= k0 + int(os.environ.get("BDSLACK", -1)) and shown < top):
                print('   %5d %s | %s' % (r[2]['total'], r[1], bdlib.fmt(r[2])[:120]))
                shown += 1


if __name__ == '__main__':
    main()
