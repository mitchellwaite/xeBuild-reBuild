"""bdlib for options: compile a source text and compare with build/op/reference.o (a copy of
the last matching build/obj/options.o).

python tools/wip/dehint/optlib.py <file.c> [-p N|-np] [-v [fn]] [-L]
  -p N  builtin-expect-probability=N (default 83, as build.sh); -np for plain -O3.
Same report as bdlib.py; .text.startup is compared too."""
import difflib, os, re, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib

R = bdlib.R
BUILD = os.path.join(R, 'build', 'op')
REF = os.path.join(BUILD, 'reference.o')
SRC = os.path.join(R, 'src', 'options.c')
os.makedirs(BUILD, exist_ok=True)
P83 = ['--param', 'builtin-expect-probability=83']
SECS = ('.text', '.text.startup', '.data', '.rdata', '.bss')

read_src = bdlib.read_src
fmt = bdlib.fmt
norm = bdlib.norm
PART = re.compile(r'\.part\.\d+')


def disasm(o):
    """bdlib.disasm with gcc's clone numbers and the cold section's name normalised: a
    split that gcc makes itself is `.part.N` in .text.unlikely, the hand-written one
    `.part.0` in .text.startup; ld puts both at the same place (`*(.text.*)`)"""
    fns, order = bdlib.disasm(o)
    f2 = {}
    for n, ls in fns.items():
        f2[PART.sub('.part', n)] = [l.replace('.text.unlikely', '.text.startup') for l in ls]
    return f2, [PART.sub('.part', n) for n in order]


def section(o, s):
    b = bdlib.section(o, s)
    if s == '.text.startup' and not b:
        b = bdlib.section(o, '.text.unlikely')
    return b
cleanup = bdlib.cleanup

bdlib.BUILD = BUILD
_ref = {}
_ref['fns'], _ref['order'] = disasm(REF)
_ref['bytes'] = open(REF, 'rb').read()
_ref['sec'] = {s: section(REF, s) for s in SECS}
_ref['rel'] = None


def relocs(o):
    t = subprocess.run([bdlib.OBJDUMP, '-r', o], capture_output=True, text=True).stdout
    return [l for l in t.split('\n') if l and not l.startswith(('In archive', o))]


_ref['rel'] = relocs(REF)


def compile_src(text, flags=P83, keep=None, extra=(), asm=False):
    d = tempfile.mkdtemp(dir=BUILD, prefix='t')
    o = keep or os.path.join(d, 'o.s' if asm else 'o.o')
    src = '#line 1 "options.c"\n' + text
    r = subprocess.run([bdlib.GCC, '-S' if asm else '-c', '-O3'] + list(flags) + list(extra) +
                       ['-I' + os.path.join(R, 'src'), '-x', 'c', '-', '-o', o],
                       input=src.encode(), cwd=d, capture_output=True)
    if r.returncode:
        return False, r.stderr.decode(errors='replace'), d
    return True, o, d


def report(o):
    r = _ref
    b = open(o, 'rb').read()
    if b == r['bytes']:
        return True, 0, {}, ['BYTES']
    fns, order = disasm(o)
    per = {}
    for n in r['order']:
        if n not in fns:
            per[n] = 9999
        else:
            k = bdlib.fdiff(r['fns'][n], fns[n])
            if k:
                per[n] = k
    notes = []
    for n in order:
        if n not in r['fns']:
            notes.append('new fn ' + n)
            per[n] = 9999
    if order != r['order'] and sorted(order) == sorted(r['order']):
        notes.append('text order differs')
    for s in SECS:
        if section(o, s) != r['sec'][s]:
            notes.append(s + ' differs')
    if relocs(o) != r['rel']:
        notes.append('relocs differ')
    return not per and not notes, sum(per.values()), per, notes


def score_text(text, flags=P83, keep=None, extra=()):
    ok, o, d = compile_src(text, flags, keep=keep, extra=extra)
    try:
        if not ok:
            return {'compile': o[:400]}
        idn, tot, per, notes = report(o)
        return {'identical': idn, 'total': tot, 'per': per, 'notes': notes}
    finally:
        cleanup(d)


def vdiff(text, flags=P83, only=None):
    ok, o, d = compile_src(text, flags)
    if not ok:
        print('COMPILE ERROR', o)
        return
    idn, tot, per, notes = report(o)
    print('IDENTICAL ' + ' '.join(notes) if idn else '%d %s %s' % (tot, per, ' '.join(notes)))
    fns, _ = disasm(o)
    for n in per:
        if only and n != only:
            continue
        if n in fns and n in _ref['fns']:
            print('=====', n, '(- reference, + draft)')
            for l in difflib.unified_diff(norm(_ref['fns'][n]), norm(fns[n]), lineterm='', n=2):
                if not l.startswith(('---', '+++')):
                    print(l)
    cleanup(d)


if __name__ == '__main__':
    a = sys.argv[1:]
    path = a.pop(0)
    flags = P83
    if '-np' in a:
        a.remove('-np')
        flags = []
    if '-L' in a:
        a.remove('-L')
        os.environ['BDLOOSE'] = '1'
    if '-p' in a:
        i = a.index('-p')
        flags = ['--param', 'builtin-expect-probability=' + a[i + 1]]
        del a[i:i + 2]
    only = None
    if '-v' in a:
        i = a.index('-v')
        only = a[i + 1] if i + 1 < len(a) else None
        vdiff(read_src(path), flags, only)
    else:
        print(fmt(score_text(read_src(path), flags)))
