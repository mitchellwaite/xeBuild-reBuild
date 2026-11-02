# gen.py: lever generator + evaluator over best34.c
# edits: ('c',line,span,form) k-lever on condition span (-1 whole) A=(t && !k) C=(k || t)
#        ('l',line,attr)      hot/cold label at statement line
#        ('f',src,tgt,kind)   dead `if (k) goto T;` (kind k) or empty asm goto (kind a) before statement src
import re, os, sys, subprocess, hashlib, json
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = open(os.path.join(HERE, os.environ.get('GBASE','baseA.c'))).read().split('\n')
CRE = re.compile(r'^(\s*(?:\} else |AT\(\w+\) )?if )\((.*)\)(\s*\{?)$')

def func_ranges():
    ce = [i for i, x in enumerate(BASE) if x.startswith('static void clientEraseBlockI(')][0]
    ce_end = [i for i in range(ce, len(BASE)) if BASE[i] == '}'][0]
    mk = [i for i, x in enumerate(BASE) if 'int kk = __builtin_constant_p(argc);' in x][0]
    mc_end = [i for i, x in enumerate(BASE) if x.startswith('fail: __attribute__((cold));')][0]
    ck = [i for i in range(ce, ce_end) if 'int kk = __builtin_constant_p(block);' in BASE[i]][0]
    return {'ce': (ck + 1, ce_end), 'mc': (mk + 1, mc_end)}
FR = func_ranges()
def fn_of(i):
    for f, (a, b) in FR.items():
        if a <= i < b: return f

def spans(c):
    """all sub-term spans (start,end) of condition c, excluding the whole"""
    out = []
    def split(a, b):
        # split c[a:b] at depth-0 || / &&
        terms = []; d = 0; s = a; i = a
        while i < b:
            ch = c[i]
            if ch in '([': d += 1
            elif ch in ')]': d -= 1
            elif ch == "'":
                i = c.index("'", i + 1)
            elif ch == '"':
                i = c.index('"', i + 1)
            elif d == 0 and c[i:i+2] in ('||', '&&'):
                terms.append((s, i)); s = i + 2; i += 2; continue
            i += 1
        terms.append((s, b))
        return terms
    def strip(a, b):
        while a < b and c[a] == ' ': a += 1
        while b > a and c[b-1] == ' ': b -= 1
        return a, b
    def rec(a, b, top):
        ts = [strip(x, y) for x, y in split(a, b)]
        if len(ts) > 1 or not top:
            for t in ts:
                if (t[0], t[1]) != (0, len(c)) and t not in out: out.append(t)
        for x, y in ts:
            seg = c[x:y]
            m = re.match(r'^(E\(|\()', seg)
            if m and seg.endswith(')'):
                # matching paren must close at end
                d = 0
                for j, ch in enumerate(seg):
                    if ch == '(': d += 1
                    elif ch == ')':
                        d -= 1
                        if d == 0: break
                if j == len(seg) - 1:
                    rec(x + len(m.group(1)), y - 1, False)
    rec(0, len(c), True)
    return out

def cond_lines():
    r = {}
    for f, (a, b) in FR.items():
        for i in range(a, b):
            m = CRE.match(BASE[i])
            if m: r[i] = m
    return r
CL = cond_lines()

def stmt_lines():
    r = []
    for f, (a, b) in FR.items():
        for i in range(a, b):
            x = BASE[i].strip()
            if not x or i in CL: continue
            if x.startswith(('}', 'else', 'for ', 'case ', 'default', 'switch', 'rok:', 'fail:', 'JUMP', 'int ', 'char ', '#', '/*', '*')): continue
            if x.endswith(';') or (x.startswith('{') and x.endswith('}')):
                if x.startswith('{') and not x.endswith('}'): continue
                r.append(i)
    return r
SL = stmt_lines()

def labname(i): return 'S%d' % i

def render(edits):
    s = list(BASE)
    ce = {}; lab = {}; feeds = {}; tgts = set()
    for e in edits:
        if e[0] == 'c': ce.setdefault(e[1], []).append((e[2], e[3]))
        elif e[0] == 'l': lab[e[1]] = e[2]
        elif e[0] == 'f':
            feeds.setdefault(e[1], []).append((e[2], e[3]))
            if isinstance(e[2], int): tgts.add(e[2])
    for i, lst in ce.items():
        m = CL[i]; c = m.group(2); sp = spans(c)
        reps = []
        for sid, fm in lst:
            a, b = (0, len(c)) if sid == -1 else sp[sid]
            reps.append((a, b, fm))
        reps.sort()
        for x, y in zip(reps, reps[1:]):
            if x[1] > y[0]: return None
        for a, b, fm in sorted(reps, reverse=True):
            t = c[a:b]
            c = c[:a] + ('(%s && !kk)' % t if fm == 'A' else '(kk || %s)' % t) + c[b:]
        s[i] = m.group(1) + '(' + c + ')' + m.group(3)
    for i in set(lab) | set(feeds) | tgts:
        x = s[i]; ind = x[:len(x) - len(x.lstrip())]; body = x.strip()
        pre = ''
        if i in tgts or i in lab:
            pre += labname(i) + ':' + (' __attribute__((%s))' % lab[i] if i in lab else '') + '; '
        for t, kind in feeds.get(i, []):
            tn = t if isinstance(t, str) else labname(t)
            pre += ('if (kk) goto %s; ' % tn) if kind == 'k' else ('__asm__ goto ("" :::: %s); ' % tn)
        s[i] = ind + '{ ' + pre + body + ' }'
    return '\n'.join(s)

def all_singles(feedtgts=None):
    E = []
    for i, m in CL.items():
        for sid in [-1] + list(range(len(spans(m.group(2))))):
            for fm in 'AC': E.append(('c', i, sid, fm))
    for i in SL:
        for a in ('hot', 'cold'): E.append(('l', i, a))
    for i in SL:
        f = fn_of(i)
        T = [j for j in SL if fn_of(j) == f and j != i] + (['rok', 'fail'] if f == 'mc' else [])
        if feedtgts is not None: T = [t for t in T if t in feedtgts]
        for t in T:
            for kind in 'ka': E.append(('f', i, t, kind))
    return E

def key(edits): return json.dumps(sorted(json.dumps(list(e)) for e in edits))
CACHE = os.path.join(HERE, os.environ.get('GCACHE','cache.jsonl'))
def load_cache():
    d = {}
    if os.path.exists(CACHE):
        for l in open(CACHE):
            try: k, v = json.loads(l); d[k] = v
            except Exception: pass
    return d

def evaluate(edits, tag='x'):
    src = render(edits)
    if src is None: return (9999, 9999)
    h = hashlib.md5(src.encode()).hexdigest()[:12]
    p = os.path.join(HERE, 'v', 'g_%s' % h)
    if not os.path.exists(p + '.res'):
        open(p + '.c', 'w', newline='\n').write(src)
        open(p + '.ref', 'w', newline='\n').write(open(os.path.join(HERE, 'c0.ref')).read())
        r = subprocess.run([r'C:\Program Files\Git\bin\sh.exe', os.path.join(HERE, '..', '..', 's101', 'f2.sh').replace('\\', '/'), (p + '.c').replace('\\', '/')], capture_output=True, text=True).stdout.strip()
        f2 = int(r) if r.isdigit() else 9999
        hk = 9999
        if f2 < 9999:
            d = subprocess.run(['diff', p + '.ref', p + '.mine'], capture_output=True, text=True).stdout
            hk = sum(1 for l in d.split('\n') if l and l[0].isdigit())
        open(p + '.res', 'w').write('%d %d' % (f2, hk))
        for ext in ('.d',):
            pass
    f2, hk = map(int, open(p + '.res').read().split())
    with open(CACHE, 'a') as fo: fo.write(json.dumps([key(edits), [f2, hk, h]]) + '\n')
    return (f2, hk)

if __name__ == '__main__':
    if sys.argv[1] == 'count':
        E = all_singles(); import collections
        print(len(E), collections.Counter(e[0] for e in E), len(CL), len(SL))
    elif sys.argv[1] == 'show':
        print(render(json.loads(sys.argv[2])))
    elif sys.argv[1] == 'spans':
        for i, m in CL.items():
            c = m.group(2); print(i + 1, [c[a:b] for a, b in spans(c)])
