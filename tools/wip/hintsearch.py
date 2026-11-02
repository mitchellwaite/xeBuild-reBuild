"""hintsearch.py <obj> [ifs] [pairs]: find hints in src/<obj>.c that can go.

Run after a matching sh build.sh (it compares against build/obj/<obj>.o).  Tries
removing each hint site alone (expect, empty asm, attributes, constant_p tests,
aliases, build.sh flags), keeps those that leave the object unchanged, repeats to
a fixpoint.  ifs also tries deleting every if statement; pairs then tries every
pair of what's left.  Writes build/hintsearch/hs_<obj>.c, the reduced source, and
lists the closest misses.  Review it before copying it back: an ifs removal can
cut into an unused macro, and a removed asm output can leave a variable unset.
The full build's SHA256 still has the last word."""
import itertools, json, os, re, subprocess, sys, difflib
from multiprocessing import Pool
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TC = os.path.join(R, 'tools', 'toolchain-4745', 'mingw32', 'bin')
os.environ['PATH'] = TC + os.pathsep + os.environ['PATH']
HERE = os.path.join(R, 'build', 'hintsearch')
os.makedirs(HERE, exist_ok=True)


def build_flags(o):
    """the object's non-default flags, from build.sh"""
    t = open(os.path.join(R, 'build.sh'), newline='').read()
    m = re.search(r'^\s*%s\) orig="\$f\.c"\s*\n\s*cflags="([^"]*)"' % re.escape(o), t, re.M)
    if not m:
        return []
    return [x for x in m.group(1).split() if x != '-O3']


def balanced(s, i):
    """s[i] == '('; index just past its match."""
    d = 0
    q = None
    k = i
    while k < len(s):
        c = s[k]
        if q:
            if c == chr(92):
                k += 1
            elif c == q:
                q = None
        elif c in '"' + "'":
            q = c
        elif c == '(':
            d += 1
        elif c == ')':
            d -= 1
            if d == 0:
                return k + 1
        k += 1
    return -1


def strip_comments(src):
    # same-length mask so offsets line up
    out = list(src)
    for m in re.finditer(r'/\*.*?\*/|//[^\n]*', src, re.S):
        for k in range(m.start(), m.end()):
            if out[k] != '\n':
                out[k] = ' '
    return ''.join(out)


def sites(src):
    """list of (id, start, end, replacement, label) as source edits, plus renames"""
    mask = strip_comments(src)
    res = []
    for m in re.finditer(r'__builtin_expect\s*\(', mask):
        o = m.end() - 1
        e = balanced(mask, o)
        depth = 0
        k = o + 1
        q = None
        while k < e:
            c = mask[k]
            if q:
                if c == q:
                    q = None
            elif c in '"' + "'":
                q = c
            elif c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
            elif c == ',' and depth == 0:
                break
            k += 1
        res.append((m.start(), e, src[o + 1:k], 'expect'))
    for m in re.finditer(r'__builtin_assume_aligned\s*\(', mask):
        o = m.end() - 1
        e = balanced(mask, o)
        k = mask.rfind(',', o, e)
        res.append((m.start(), e, src[o + 1:k], 'assume'))
    for m in re.finditer(r'\b__builtin_prefetch\s*\(', mask):
        e = balanced(mask, m.end() - 1)
        res.append((m.start(), e, '(void)0', 'prefetch'))
    for m in re.finditer(r'__asm__\s*(goto\s*)?\(\s*""', mask):
        o = mask.index('(', m.start())
        e = balanced(mask, o)
        res.append((m.start(), e, '(void)0', 'asm'))
    for m in re.finditer(r'\bJMP\s*\(', mask):
        if mask[:m.start()].endswith('#define '):
            continue
        e = balanced(mask, m.end() - 1)
        res.append((m.start(), e, '(void)0', 'JMP'))
    for m in re.finditer(r'__attribute__\s*\(\(', mask):
        o = mask.index('(', m.start())
        e = balanced(mask, o)
        inner = src[o + 2:e - 2]
        if inner.startswith('optimize') and inner.count('"') > 2:
            ops = re.findall(r'"[^"]*"', inner)
            for x in ops:
                rest = ', '.join(y for y in ops if y != x)
                res.append((m.start(), e, f'__attribute__((optimize({rest})))', 'attr-' + x))
        res.append((m.start(), e, '', 'attr ' + inner[:30]))
    for m in re.finditer(r'if\s*\(', mask):
        o = m.end() - 1
        e = balanced(mask, o)
        if e < 0:
            continue
        cond = mask[o:e]
        rest = mask[e:e + 40].lstrip()
        if rest.startswith('__builtin_unreachable'):
            semi = mask.index(';', e)
            res.append((m.start(), semi + 1, '', 'unreach'))
        elif re.search(r'__builtin_constant_p|\bcp\(', cond) and not rest.startswith('{'):
            semi = mask.index(';', e)
            if '\n\n' not in mask[e:semi]:
                res.append((m.start(), semi + 1, '', 'cp'))
    for m in re.finditer(r'\b\w*_hint\s*\(', mask):
        e = balanced(mask, m.end() - 1)
        ls = mask.rfind('\n', 0, m.start()) + 1
        if mask[ls:m.start()].strip() == '' and mask[e:e + 1] == ';':
            res.append((m.start(), e, '(void)0', 'hintcall'))
    for m in re.finditer(r'^#define XB_(PATCHES|FILES_BOUND).*$', mask, re.M):
        res.append((m.start(), m.end(), '', 'define'))
    for m in re.finditer(r'\bE\s*\(', mask):
        if mask[:m.start()].endswith('#define '):
            continue
        e = balanced(mask, m.end() - 1)
        res.append((m.start(), e, src[m.end():e - 1], 'E'))
    if IFS:
        for m in re.finditer(r'\bif\s*\(', mask):
            o = m.end() - 1
            e = balanced(mask, o)
            if e < 0:
                continue
            k = e
            while k < len(mask) and mask[k].isspace():
                k += 1
            if mask[k] == '{':
                d = 0
                q = k
                while q < len(mask):
                    if mask[q] == '{':
                        d += 1
                    elif mask[q] == '}':
                        d -= 1
                        if d == 0:
                            break
                    q += 1
                end = q + 1
            else:
                if re.match(r'(if|for|while|switch|do)\b', mask[k:k + 8]):
                    continue
                end = mask.find(';', k) + 1
                if end <= 0:
                    continue
            nxt = mask[end:end + 12].lstrip()
            if nxt.startswith('else'):
                continue
            before = mask[:m.start()].rstrip()
            if before.endswith('else'):
                continue
            if end - m.start() > 4000:
                continue
            res.append((m.start(), end, '', 'ifdel'))
    al = []
    for m in re.finditer(r'^[^\n;{}]*?\b(\w+)\s*\([^;{}]*\)\s*__asm__\s*\(\s*"_([\w.]+)"\s*\)[^;]*;', mask, re.M):
        al.append((m.group(1), m.group(2), m.start(), m.end()))
    return sorted(res), al


def norm(path):
    out = subprocess.run([TC + r'\objdump.exe', '-dr', '--no-show-raw-insn', path], capture_output=True, text=True).stdout
    fs = {}
    cur = None
    for l in out.splitlines():
        m = re.match(r'^[0-9a-f]+ <(.*)>:', l)
        if m:
            cur = m.group(1)
            fs[cur] = []
            continue
        if cur is None or not l.strip():
            continue
        l = re.sub(r'^\s*[0-9a-f]+:\s*', '', l)
        l = re.sub(r'\b(j\w+|call)\s+[0-9a-f]+ <([^>+]*)(\+0x[0-9a-f]+)?>', r'\1 \2', l)
        fs[cur].append(l)
    return fs


def data(path):
    return subprocess.run([TC + r'\objdump.exe', '-s', '-j', '.rdata', '-j', '.data', path], capture_output=True, text=True).stdout.split('\n', 2)[-1]


def bss(path):
    t = subprocess.run([TC + r'\objdump.exe', '-h', path], capture_output=True, text=True).stdout
    m = re.search(r'\.bss\s+([0-9a-f]+)', t)
    return m.group(1) if m else ''


obj = sys.argv[1]
IFS = 'ifs' in sys.argv
PAIRS = 'pairs' in sys.argv
BASEO = os.path.join(R, 'build', 'obj', obj + '.o')
BASE = norm(BASEO)
BASED = data(BASEO)
BASEB = bss(BASEO)


def compile_(code, flags):
    tag = '%s_%d' % (obj, os.getpid())
    tmp = os.path.join(HERE, 'hs_t_' + tag + '.c')
    out = os.path.join(HERE, 'hs_t_' + tag + '.o')
    open(tmp, 'w', newline='').write('#line 1 "%s.c"\n' % obj + code)
    r = subprocess.run([TC + r'\gcc.exe', '-c'] + flags + ['-I' + R + r'\src', tmp, '-o', out], capture_output=True, text=True)
    if r.returncode:
        return None
    t = norm(out)
    fns = {}
    for f in BASE:
        if BASE[f] != t.get(f):
            if len(BASE[f]) + len(t.get(f, [])) > 6000:
                fns[f] = 999
            else:
                fns[f] = sum(1 for x in difflib.ndiff(BASE[f], t.get(f, [])) if x[0] in '+-')
    extra = [f for f in t if f not in BASE]
    return sum(fns.values()) + len(extra) * 100, fns, data(out) != BASED


def apply(src, edits):
    """edits: (start, end, repl) non-overlapping"""
    out = src
    for s, e, r in sorted(edits, key=lambda x: -x[0]):
        out = out[:s] + r + out[e:]
    return out


def make(src, flags, pick):
    """pick: list of ('s', site) / ('a', alias) / ('f', flags-item)"""
    fl = list(flags)
    edits = []
    renames = []
    for kind, x in pick:
        if kind == 's':
            edits.append((x[0], x[1], x[2]))
        elif kind == 'a':
            edits.append((x[2], x[3], ''))
            renames.append((x[0], x[1]))
        else:
            idx = fl.index(x)
            if x == '--param':
                pass
            fl = remove_flag(fl, x)
    # overlap check
    ed = sorted(edits)
    for a, b in zip(ed, ed[1:]):
        if a[1] > b[0]:
            return None, None
    code = apply(src, edits)
    for a, b in renames:
        code = re.sub(r'\b%s\b' % re.escape(a), b, code)
    return code, fl


def remove_flag(fl, x):
    out = []
    i = 0
    while i < len(fl):
        if fl[i] == '--param' and fl[i + 1] == x:
            i += 2
            continue
        if fl[i] == x:
            i += 1
            continue
        out.append(fl[i])
        i += 1
    return out


def flag_items(fl):
    out = []
    i = 0
    while i < len(fl):
        if fl[i] == '--param':
            out.append(fl[i + 1])
            i += 2
        else:
            out.append(fl[i])
            i += 1
    return out


def job(a):
    src, flags, pick = a
    code, fl = make(src, flags, pick)
    if code is None:
        return None
    r = compile_(code, ['-O3'] + fl)
    return r


def label(src, p):
    k, x = p
    if k == 's':
        return '%d:%s' % (src.count('\n', 0, x[0]) + 1, x[3])
    if k == 'a':
        return 'alias ' + x[0]
    return 'flag ' + x


def candidates(src, flags):
    s, al = sites(src)
    return [('s', x) for x in s] + [('a', x) for x in al] + [('f', x) for x in flag_items(flags)]


def main():
    src = open(R + '\\src\\' + obj + '.c', newline='').read()
    flags = build_flags(obj)
    r0 = compile_(src, ['-O3'] + flags)
    assert r0 and r0[0] == 0 and not r0[2], ('baseline differs', r0)
    log = []
    with Pool() as p:
        removed = []
        while True:
            c = candidates(src, flags)
            res = p.map(job, [(src, flags, [x]) for x in c], chunksize=1)
            free = [x for x, r in zip(c, res) if r and r[0] == 0 and not r[2]]
            near = sorted([(r[0], r[2], label(src, x), r[1]) for x, r in zip(c, res) if r and (r[0] or r[2])], key=lambda t: t[0])
            print(obj, 'candidates', len(c), 'free', [label(src, x) for x in free], flush=True)
            if not free:
                break
            free.sort(key=lambda x: -x[1][0] if x[0] == 's' else 1)
            for x in free:
                if x[0] != 's':
                    continue
                code, fl = make(src, flags, [x])
                if code is None:
                    continue
                r = compile_(code, ['-O3'] + fl)
                if r and r[0] == 0 and not r[2]:
                    removed.append(label(src, x))
                    src, flags = code, fl
            if all(x[0] != 's' for x in free):
                x = free[0]
                code, fl = make(src, flags, [x])
                removed.append(label(src, x))
                src, flags = code, fl
            continue
        print('REMOVED', removed, flush=True)
        print('flags now', flags)
        open(os.path.join(HERE, 'hs_%s.c' % obj), 'w', newline='').write(src)
        json.dump({'flags': flags, 'removed': removed}, open(os.path.join(HERE, 'hs_%s.json' % obj), 'w'))
        print('--- nearest single removals')
        for t in near[:25]:
            print(t[0], 'data' if t[1] else '', t[2], {k: v for k, v in list(t[3].items())[:4]})
        if PAIRS:
            c = candidates(src, flags)
            pairs = list(itertools.combinations(c, 2))
            print('pairs', len(pairs), flush=True)
            res = p.map(job, [(src, flags, list(x)) for x in pairs], chunksize=4)
            ok = [(label(src, a), label(src, b)) for (a, b), r in zip(pairs, res) if r and r[0] == 0 and not r[2]]
            print('PAIR MATCHES', ok)
            sing = sorted([(r[0], r[2], label(src, a), label(src, b)) for (a, b), r in zip(pairs, res) if r and (r[0] or r[2])], key=lambda t: t[0])
            for t in sing[:10]:
                print(t)


if __name__ == '__main__':
    main()
