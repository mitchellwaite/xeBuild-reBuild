"""mode_client attempt 1: ablate the hints in src/mode_client.c one at a time, then greedily.

python tools/wip/dehint/mc1.py list                     the slots and their variants
python tools/wip/dehint/mc1.py singles [-j N]           every variant alone -> build/mc/singles.json
python tools/wip/dehint/mc1.py greedy [-j N]            accumulate free variants -> build/mc/greedy.json
python tools/wip/dehint/mc1.py show STATE.json [-o out.c] [-v [fn]]   render/score a state
python tools/wip/dehint/mc1.py count [file.c]           trick count by category

The base text (src/mode_client.c, or MCBASE=<file>) is cut into a template: plain text and
slots.  A slot has variants (0 = the original text); a list slot (asm goto label lists,
the literal-order asm's operands) drops elements.  A state is {slot: variant} plus
{listslot: [dropped labels]}.  Comparison: mc1lib (whole object vs build/mc/reference.o)."""
import json, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib

BASE = os.environ.get('MCBASE', mc1lib.SRC)
OUT = mc1lib.BUILD

CP = '__builtin_constant_p'


# ---------------------------------------------------------------- template
class T:
    def __init__(self, text):
        self.parts = [text]       # str or ('v', name) or ('l', name)
        self.var = {}             # name -> [text0, text1, ...]
        self.lists = {}           # name -> (prefix, [labels], sep, suffix)
        self.line = {}

    def _split(self, pat, make, flags=0):
        """replace matches of pat in the str parts by slots; make(m) -> list of parts"""
        out = []
        for p in self.parts:
            if not isinstance(p, str):
                out.append(p)
                continue
            k = 0
            for m in re.finditer(pat, p, flags):
                r = make(m)
                if r is None:
                    continue
                out.append(p[k:m.start()])
                out.extend(r)
                k = m.end()
            out.append(p[k:])
        self.parts = out

    def slot(self, name, variants):
        assert name not in self.var and name not in self.lists, name
        self.var[name] = variants
        return [('v', name)]

    def lslot(self, name, prefix, labels, sep, suffix, empty=''):
        assert name not in self.var and name not in self.lists, name
        self.lists[name] = (prefix, labels, sep, suffix, empty)
        return [('l', name)]

    def render(self, state=None, drops=None):
        state = state or {}
        drops = drops or {}
        o = []
        for p in self.parts:
            if isinstance(p, str):
                o.append(p)
            elif p[0] == 'v':
                o.append(self.var[p[1]][state.get(p[1], 0)])
            else:
                pre, labs, sep, suf, empty = self.lists[p[1]]
                d = set(drops.get(p[1], ()))
                keep = [l for l in labs if l not in d]
                o.append(pre + sep.join(keep) + suf if keep else empty)
        return ''.join(o)


def lineof(text, s):
    return text[:text.find(s)].count('\n') + 1


def build_template(text):
    t = T(text)
    n = [0]

    def lit(name, old, *alts):
        """a literal slot: old must occur once in the str parts"""
        hits = sum(p.count(old) for p in t.parts if isinstance(p, str))
        assert hits <= 1, (name, hits)
        if not hits:
            return
        t._split(re.escape(old), lambda m: t.slot(name, [old] + list(alts)))

    # --- manual slots (before the automatic ones, so they keep their insides)
    lit('ceb_kk', '\tint kk = __builtin_constant_p(block);\n', '')
    lit('ceb_efail', '{ AT(efail) log_printf', '{ log_printf')
    lit('cebi_efcl', ' efcl: asm volatile("" : : "i"(64));', '')
    lit('cebi_dy', 'if (0) { dy: asm volatile(""); if (__builtin_constant_p(block + 901)) goto ybk; __builtin_unreachable(); } ',
        '', 'if (0) { dy: asm volatile(""); __builtin_unreachable(); } ')
    lit('mc_kk', '\tint kk = __builtin_constant_p(argc);\n', '')
    lit('bp_pin', '\t\t\t__asm__("" :: "a"(i + 1));\n', '')
    lit('r_memset', '__builtin_memset(argv, 0, kk); ', '')
    lit('r_ifkk', 'if (!kk) { ac: __attribute__((cold)); __asm__ goto ("" :: "a"(i) :: r5x, r3x); } ',
        '',
        'if (!kk) { __asm__ goto ("" :: "a"(i) :: r5x, r3x); } ',
        'if (!kk) { ac: __attribute__((cold)); __asm__ goto ("" :::: r5x, r3x); } ',
        'if (!kk) { ac: __attribute__((cold)); __asm__ goto ("" :: "a"(i) :: r5x); } ',
        'if (!kk) { ac: __attribute__((cold)); __asm__ goto ("" :: "a"(i) :: r3x); } ',
        'if (!kk) { ac: __attribute__((cold)); } ')
    d1 = 'i + 1 == argc || ({ __asm__ ("" :: "d"(i + 1)); 0; }) || *argv[i + 1]'
    # two identical occurrences: cut them by context
    parts = []
    k = 0
    for p in t.parts:
        if not isinstance(p, str):
            parts.append(p)
            continue
        while True:
            j = p.find(d1)
            if j < 0:
                break
            nm = 'i_dpin' if p.find('info dump path', j) < p.find('patch file set', j) or p.find('patch file set', j) < 0 else 'p_dpin'
            if nm in t.var:
                nm = 'p_dpin'
            parts.append(p[:j])
            parts.extend(t.slot(nm, [d1, 'i + 1 == argc || *argv[i + 1]']))
            p = p[j + len(d1):]
        parts.append(p)
    t.parts = parts
    dblk = '\t\t\t\t\t{ int r; __asm__ volatile("" : "=D"(r)); __asm__ volatile("" :: "D"(r)); }\n'
    lit('bp_D', dblk + dblk, dblk, '')
    lit('bp_rcount', '\t\t\t\t\t__asm__("" :: "r"(count));\n', '')
    lit('ci_lit', '\t\t/* .rdata order hint (testing success first flips the branch) */\n\t\t__asm__("" :: "i"("success!\\n"));\n', '')
    # clientWriteBlocks' literal-order asm: a list of "i" operands
    wb_old = re.search(r'\t/\* \.rdata order hint: these come before the read error.*?\n\t__asm__\("" :: (.*?)\);\n', text, re.S)
    if wb_old:  # gone since attempt 2
        ops = re.findall(r'"i"\(".*?"\)', wb_old.group(1))
        head = wb_old.group(0)[:wb_old.group(0).find('__asm__')]
        t._split(re.escape(wb_old.group(0)), lambda m: t.lslot('wb_lit', head + '__asm__("" :: ', ops, ',\n\t\t', ');\n'))
    lit('fk_X', '__asm__ ("" :: "X"(&fko), "X"(&fkv)); ', '')
    lit('rk_m', '__asm__ ("" :: "m"(rko), "m"(rkv2)); ', '')
    m = re.search(r'rkn0: ; \{ struct \{\} rkv1; goto rkn1; .*? \} rkn1: ; ', text)
    if m:
        lit('rk_dead1', m.group(0), 'rkn0: ; ')
    rok_all = fk_all = None
    lit('dv', 'if (0) { dv: asm volatile("" : : : "memory");  __builtin_unreachable(); } ', '')
    lit('dz', 'if (0) { dz: asm volatile("" : : : "cc"); __builtin_unreachable(); } ', '')
    m = re.search(r'if \(__builtin_constant_p\(mode \+ 1210\).*? mode = 9; ', text)
    if m and os.environ.get('MCCHAIN') == 'lists':
        # each arm's terms as a list slot (all dropped: compile error, so never taken)
        for arm in re.finditer(r'if \((.*?)\) mode = (\d+);', m.group(0)):
            terms = arm.group(1).split(' && ')
            t._split(re.escape(arm.group(0)), lambda k, terms=terms, arm=arm: t.lslot(
                'mc_arm%s' % arm.group(2), 'if (', terms, ' && ', ') mode = %s;' % arm.group(2), 'if () error;'))
    elif m:
        chain = m.group(0)
        arms = re.findall(r'if \((.*?)\) mode = (\d+);', chain)
        def ch(sel):
            a = [x for x in arms if x[1] in sel]
            return ' else '.join('if (%s) mode = %s;' % x for x in a) + (' ' if a else '')
        lit('mode_chain', chain, '', ch('711'), ch('7'), ch('119'), ch('79'), ch('9'), ch('11'))

    # --- whole-construct removals of the trampolines are tried via the 'big' slots below:
    # rok_all / fk_all are left in place (their pieces are slots); see singles' extra edits.

    # --- automatic: cp feeds `if (cp && cp ...) goto L;`
    def feed(m):
        cond, tgt = m.group(1), m.group(2)
        if CP not in cond or 'strnicmp' in cond:
            return None
        terms = re.split(r' && ', cond)
        name = 'cp_%s_%d' % (tgt, n[0])
        n[0] += 1
        if len(terms) == 1:
            return t.slot(name, [m.group(0), ''])
        return t.lslot(name, 'if (', terms, ' && ', ') goto %s;' % tgt)
    t._split(r'if \(((?:[^;{}])*?)\) goto (\w+);', feed)

    # --- automatic: asm goto label lists
    def jl(m):
        labs = [x.strip() for x in m.group(2).split(',')]
        name = 'j_%s_%d' % (labs[0], n[0])
        n[0] += 1
        return t.lslot(name, m.group(1), labs, ', ' if ', ' in m.group(2) else ',', m.group(3))
    t._split(r'(JMP\()([\w, ]+)(\);)', jl)
    t._split(r'(__asm__ goto \("" [^;]*?: ?: ?)([\w, ]+)(\);)', jl)

    # --- automatic: cold labels
    def cold(m):
        name = 'cold_%s' % m.group(1)
        return t.slot(name, [m.group(0), '', m.group(1) + ':'])
    t._split(r'\{ (\w+): __attribute__\(\(cold\)\); \}', cold)
    t._split(r'(\w+): __attribute__\(\(cold\)\);', cold)

    # --- automatic: expects
    def ex(m):
        name = 'E_%s' % re.sub(r'\W', '', m.group(1))[-8:]
        return t.slot(name, [m.group(0), m.group(1)])
    t._split(r'\bE\(((?:[^()]|\([^()]*(?:\([^()]*\))?[^()]*\))*)\)', ex)
    t.big = {'rok_all': rok_all, 'fk_all': fk_all}
    return t


# ---------------------------------------------------------------- counting
def strip_comments(s):
    return re.sub(r'/\*.*?\*/', '', s, flags=re.S)


def count(text):
    s = strip_comments(text)
    s = re.sub(r'#define .*', '', s)
    c = {}
    c['cp'] = s.count(CP)
    c['asmgoto'] = len(re.findall(r'\bJMP\(', s)) + s.count('__asm__ goto')
    c['cold'] = s.count('__attribute__((cold))')
    c['expect'] = len(re.findall(r'\bE\(', s)) + s.count('__builtin_expect')
    c['if0'] = s.count('if (0)')
    c['unreach'] = s.count('__builtin_unreachable')
    c['litasm'] = len(re.findall(r'__asm__\("" :: "i"\("', s))
    pins = len(re.findall(r'__asm__\s*(?:volatile)?\s*\("" :: "[adDr]"\(', s))
    pins += len(re.findall(r'\{ int r; __asm__ volatile\("" : "=D"\(r\)\)', s))
    pins += len(re.findall(r'"[XmDadr]"\(&?\w+[^)]*\), "[Xm]"', s))
    pins += len(re.findall(r'__asm__ goto \("" :: "[a-d]"', s))
    c['pin'] = pins
    c['inline'] = 1 if 'clientEraseBlockI' in s else 0
    c['total'] = sum(c.values())
    return c


# ---------------------------------------------------------------- runs
def _rok_all(s):
    return re.sub(r'\{ struct \{\} rko; .*? \} rkE: ; ', '', s, count=1)


def _fk_all(s):
    return re.sub(r'fkbo: \{ struct \{\} fko; .*? fkM: ; \} fkN: ;', '', s, count=1)


def _inline(s):
    """clientEraseBlockI gone: mode_client calls clientEraseBlock"""
    i = s.find('static void clientEraseBlockI(')
    j = s.find('\n}\n', i) + 3
    s = s[:i] + s[j:].lstrip('\n')
    return s.replace('clientEraseBlockI(arg)', 'clientEraseBlock(arg)')


POST = {'rok_all': _rok_all, 'fk_all': _fk_all, 'inline': _inline}
NP = '-np'


def render(t, state, drops, post=()):
    text = t.render(state, drops)
    for p in post:
        if p != NP:
            text = POST[p](text)
    return text


def score(t, state, drops, post=()):
    text = render(t, state, drops, post)
    s = mc1lib.score_text(text, [] if NP in post else mc1lib.P50)
    s['count'] = count(text)['total'] - (1 if NP in post else 0)
    return s


def edits(t):
    """every single edit: (key, state, drops, post)"""
    out = [(p, {}, {}, [p]) for p in list(POST) + [NP]]
    # whole dead constructs: the block and every edge into it
    out.append(('G_dy', {'cebi_dy': 1, 'cp_dy_0': 1}, {'j_dy_22': ['dy']}, []))
    out.append(('G_dz', {'dz': 1}, {'j_dz_24': ['dz']}, []))
    out.append(('G_dv', {'dv': 1}, {'j_dv_32': ['dv']}, []))
    out.append(('G_efail', {}, {'j_efail_21': ['efail'], 'j_efail_23': ['efail']}, []))
    out.append(('G_kk', {'mc_kk': 1, 'r_memset': 1, 'r_ifkk': 1}, {}, []))
    out.append(('G_dpin', {'i_dpin': 1, 'p_dpin': 1}, {}, []))
    out.append(('G_hdd', {}, {'j_hdd4_25': ['hdd4', 's5', 'hdd5'], 'j_hdd4_28': ['hdd4', 'hdd5']}, []))
    out.append(('G_dsp', {}, {'j_dsp_26': ['dsp'], 'j_dsp_35': ['dsp'], 'j_dsp_36': ['dsp']}, []))
    out.append(('G_cebi', {'cebi_dy': 1, 'cp_dy_0': 1, 'cold_efc': 1, 'cold_einv': 1},
                {'j_dy_22': ['dy'], 'j_efail_21': ['efail'], 'j_efail_23': ['efail']}, ['inline']))
    out.append(('G_E', {k: 1 for k in t.var if k.startswith('E_') and k != 'E_x'}, {}, [NP]))
    for nm, vs in t.var.items():
        if nm == 'E_x':
            continue
        for k in range(1, len(vs)):
            out.append(('%s=%d' % (nm, k), {nm: k}, {}, []))
    for nm, (pre, labs, sep, suf, e) in t.lists.items():
        for l in labs:
            out.append(('%s-%s' % (nm, l), {}, {nm: [l]}, []))
        if len(labs) > 1:
            out.append(('%s-ALL' % nm, {}, {nm: list(labs)}, []))
    return out


def run_singles(t, jobs, start=None, es=None):
    start = start or ({}, {}, [])
    es = es or edits(t)
    todo = []
    for e in es:
        m = merge(start, e[1:])
        if m:
            todo.append((e[0], m))
    res = {}
    with ThreadPoolExecutor(jobs) as ex:
        for (k, m), s in zip(todo, ex.map(lambda e: score(t, *e[1]), todo)):
            res[k] = {'state': m[0], 'drops': m[1], 'post': m[2], 'r': mc1lib.fmt(s)[:300],
                      'ok': bool(s.get('identical')), 'count': s['count']}
            print('%-40s %4s %s' % (k, s['count'], mc1lib.fmt(s)[:150]), flush=True)
    return res


def run_pairs(t, jobs, start, maxdiff):
    """pairs of edits that each differ alone (diff <= maxdiff) on top of start"""
    sj = json.load(open(os.path.join(OUT, 'singles2.json')))
    es = {e[0]: e for e in edits(t)}
    near = []
    for k, r in sj.items():
        m = re.match(r'(\d+)', r['r'])
        if k in es and not r['ok'] and m and int(m.group(1)) <= maxdiff:
            near.append(k)
    todo = []
    for i in range(len(near)):
        for j in range(i + 1, len(near)):
            m = merge(start, es[near[i]][1:])
            m = m and merge(m, es[near[j]][1:])
            if m:
                todo.append((near[i] + ' + ' + near[j], m))
    print(len(near), 'near,', len(todo), 'pairs', flush=True)
    res = {}
    with ThreadPoolExecutor(jobs) as ex:
        for (k, m), s in zip(todo, ex.map(lambda e: score(t, *e[1]), todo)):
            if s.get('identical'):
                print('PAIR', k, s['count'], flush=True)
                res[k] = {'state': m[0], 'drops': m[1], 'post': m[2], 'count': s['count']}
    return res


def merge(a, b):
    """a, b: (state, drops, post); None when b conflicts with or is already in a"""
    st = dict(a[0])
    for k, v in b[0].items():
        if st.get(k, 0):
            return None
        st[k] = v
    dr = {k: list(v) for k, v in a[1].items()}
    new = False
    for k, v in b[1].items():
        old = set(dr.get(k, []))
        if not set(v) - old:
            continue
        new = True
        dr[k] = sorted(old | set(v))
    po = list(a[2])
    for p in b[2]:
        if p in po:
            return None
        po.append(p)
        new = True
    if not new and st == a[0]:
        return None
    return st, dr, po


def run_greedy(t, jobs, start=None, path=None):
    path = path or os.path.join(OUT, 'greedy.json')
    sj = os.path.join(OUT, 'singles.json')
    single = json.load(open(sj)) if os.path.exists(sj) else {}
    es = edits(t)
    def key(e):
        r = single.get(e[0])
        if not r:
            return (2, 0)
        if r['ok']:
            return (0, 0)
        m = re.match(r'(\d+)', r['r'])
        return (1, int(m.group(1)) if m else 99999)
    es.sort(key=key)
    cur = start or ({}, {}, [])
    log = []
    with ThreadPoolExecutor(jobs) as ex:
        changed = True
        while changed:
            changed = False
            i = 0
            while i < len(es):
                batch = []
                while i < len(es) and len(batch) < jobs:
                    m = merge(cur, es[i][1:])
                    if m:
                        batch.append((es[i][0], es[i][1:], m))
                    i += 1
                res = list(ex.map(lambda b: score(t, *b[2]), batch))
                good = [b for b, r in zip(batch, res) if r.get('identical')]
                for b, r in zip(batch, res):
                    print('  %-36s %s' % (b[0], mc1lib.fmt(r)[:100]), flush=True)
                if not good:
                    continue
                if len(good) > 1:
                    m = cur
                    for b in good:
                        m = merge(m, b[1]) or m
                    r = score(t, *m)
                    if r.get('identical'):
                        cur = m
                        log += [b[0] for b in good]
                        changed = True
                        print('ACCEPT', [b[0] for b in good], r['count'], flush=True)
                        json.dump({'state': cur[0], 'drops': cur[1], 'post': cur[2], 'log': log}, open(path, 'w'), indent=1)
                        continue
                for b in good:
                    m = merge(cur, b[1])
                    if not m:
                        continue
                    r = score(t, *m) if b is not good[0] or len(good) > 1 else {'identical': True, 'count': count(render(t, *m))['total']}
                    if r.get('identical'):
                        cur = m
                        log.append(b[0])
                        changed = True
                        print('ACCEPT', b[0], r['count'], flush=True)
                        json.dump({'state': cur[0], 'drops': cur[1], 'post': cur[2], 'log': log}, open(path, 'w'), indent=1)
    return cur


def main():
    a = sys.argv[1:]
    jobs = 4
    if '-j' in a:
        jobs = int(a[a.index('-j') + 1])
    text = mc1lib.read_src(BASE)
    if a[0] == 'count':
        print(count(mc1lib.read_src(a[1]) if len(a) > 1 else text))
        return
    t = build_template(text)
    assert t.render() == text, 'template does not round-trip'
    if a[0] == 'list':
        for nm, vs in t.var.items():
            print(nm, len(vs) - 1, repr(vs[0][:90]))
        for nm, l in t.lists.items():
            print(nm, l[1])
        print(count(text))
    elif a[0] in ('singles', 'pairs'):
        start = None
        if '-s' in a:
            j = json.load(open(a[a.index('-s') + 1]))
            start = (j['state'], j['drops'], j.get('post', []))
        if a[0] == 'pairs':
            res = run_pairs(t, jobs, start or ({}, {}, []), int(a[a.index('-m') + 1]) if '-m' in a else 60)
            json.dump(res, open(os.path.join(OUT, 'pairs.json'), 'w'), indent=1)
        else:
            res = run_singles(t, jobs, start)
            json.dump(res, open(os.path.join(OUT, 'singles2.json' if start else 'singles.json'), 'w'), indent=1)
    elif a[0] == 'climb':
        # greedy, then singles + pairs on top; take the pair that removes the most; repeat
        j = json.load(open(a[a.index('-s') + 1]))
        cur = (j['state'], j['drops'], j.get('post', []))
        md = int(a[a.index('-m') + 1]) if '-m' in a else 30
        rnd = 0
        while True:
            rnd += 1
            cur = run_greedy(t, jobs, cur, os.path.join(OUT, 'climb.json'))
            json.dump({'state': cur[0], 'drops': cur[1], 'post': cur[2]}, open(os.path.join(OUT, 'climb.json'), 'w'), indent=1)
            print('ROUND', rnd, count(render(t, *cur))['total'], flush=True)
            res = run_singles(t, jobs, cur)
            json.dump(res, open(os.path.join(OUT, 'singles2.json'), 'w'), indent=1)
            pr = run_pairs(t, jobs, cur, md)
            if not pr:
                break
            k = min(pr, key=lambda k: pr[k]['count'])
            print('TAKE', k, pr[k]['count'], flush=True)
            cur = (pr[k]['state'], pr[k]['drops'], pr[k]['post'])
        json.dump({'state': cur[0], 'drops': cur[1], 'post': cur[2]}, open(os.path.join(OUT, 'climb.json'), 'w'), indent=1)
        print(count(render(t, *cur)))
    elif a[0] == 'greedy':
        start = None
        if '-s' in a:
            j = json.load(open(a[a.index('-s') + 1]))
            start = (j['state'], j['drops'], j.get('post', []))
        cur = run_greedy(t, jobs, start)
        text2 = render(t, *cur)
        print(count(text2))
        print(mc1lib.fmt(score(t, *cur)))
    elif a[0] == 'show':
        j = json.load(open(a[1]))
        text2 = render(t, j.get('state'), j.get('drops'), j.get('post', ()))
        if '-o' in a:
            open(a[a.index('-o') + 1], 'w', newline='\n').write(text2)
        print(count(text2))
        if '-v' in a:
            k = a.index('-v')
            mc1lib.vdiff(text2, only=a[k + 1] if k + 1 < len(a) else None)
        else:
            print(mc1lib.fmt(mc1lib.score_text(text2)))


if __name__ == '__main__':
    main()
