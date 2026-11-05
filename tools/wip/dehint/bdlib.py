"""Shared helpers for build's de-hinting: compile a source text and compare the object with
build/bd/reference.o (a copy of the last matching build/obj/build.o).

python tools/wip/dehint/bdlib.py <file.c> [-p N|-np] [-v [fn]] [-L]
  -p N  builtin-expect-probability=N (default 98, as build.sh); -np for plain -O3.
  -v    print the per-function diff, optionally only for fn.
  -L    loose: ignore jump targets and padding when counting (BDLOOSE=1 does the same).

Report: `IDENTICAL` when all of .text/.data/.rdata/.bss and their relocations equal the
reference (`BYTES` is added when the whole file does); otherwise total differing disassembly
lines, per function, and any data section that differs.  Jump targets are kept relative to
the function, so a target change counts, and .p2align shows up as its padding's nops."""
import difflib, os, re, subprocess, sys, tempfile

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TC = os.path.join(R, 'tools', 'toolchain-4745', 'mingw32', 'bin')
os.environ['PATH'] = TC + os.pathsep + os.environ['PATH']
GCC = os.path.join(TC, 'gcc.exe')
OBJDUMP = os.path.join(TC, 'objdump.exe')
OBJCOPY = os.path.join(TC, 'objcopy.exe')
BUILD = os.path.join(R, 'build', 'bd')
REF = os.path.join(BUILD, 'reference.o')
SRC = os.path.join(R, 'src', 'build.c')
os.makedirs(BUILD, exist_ok=True)
P98 = ['--param', 'builtin-expect-probability=98']


def read_src(path=SRC):
    return open(path, newline='').read().replace('\r\n', '\n')


def compile_src(text, flags=P98, keep=None, extra=(), asm=False):
    """compile as build.sh does (stdin, #line); returns (ok, objpath or stderr, tmpdir)"""
    d = tempfile.mkdtemp(dir=BUILD, prefix='t')
    o = keep or os.path.join(d, 'o.s' if asm else 'o.o')
    src = '#line 1 "build.c"\n' + text
    r = subprocess.run([GCC, '-S' if asm else '-c', '-O3'] + list(flags) + list(extra) +
                       ['-I' + os.path.join(R, 'src'), '-x', 'c', '-', '-o', o],
                       input=src.encode(), cwd=d, capture_output=True)
    if r.returncode:
        return False, r.stderr.decode(errors='replace'), d
    return True, o, d


def cleanup(d):
    for f in os.listdir(d):
        try:
            os.remove(os.path.join(d, f))
        except OSError:
            pass
    try:
        os.rmdir(d)
    except OSError:
        pass


def disasm(o):
    """{symbol: [normalised lines]}: instruction text, relocs kept, addresses dropped;
    jump targets rewritten relative to the function start"""
    t = subprocess.run([OBJDUMP, '-d', '-r', '-M', 'intel', '--no-show-raw-insn', o],
                       capture_output=True, text=True).stdout
    fns = {}
    order = []
    cur = None
    for l in t.split('\n'):
        m = re.match(r'^([0-9a-f]+) <(.+)>:$', l)
        if m:
            cur = m.group(2)
            base = int(m.group(1), 16)
            fns[cur] = []
            order.append(cur)
            continue
        if cur is None:
            continue
        m = re.match(r'^\s*([0-9a-f]+):\s+(.*)$', l)
        if m:
            s = m.group(2).strip()
            s = re.sub(r'\b([0-9a-f]+) <[^>]*>', lambda k: '%x' % (int(k.group(1), 16) - base), s)
            fns[cur].append(s)
        elif re.match(r'^\s*[0-9a-f]+: (DISP|dir|\.)', l) or 'DISP32' in l or 'dir32' in l:
            fns[cur].append(re.sub(r'^\s*[0-9a-f]+:\s*', '', l).strip())
    return fns, order


def norm(ls):
    if os.environ.get('BDLOOSE'):
        ls = [re.sub(r'^(j\w+|call)\s+[0-9a-f]+$', r'\1', l) for l in ls]
        ls = [l for l in ls if not re.match(r'^(nop|xchg\s+ax,ax|lea\s+(esi|edi),\[(esi|edi).*\]|mov\s+esi,esi)', l)]
    return ls


def section(o, name):
    t = tempfile.mktemp(dir=BUILD)
    subprocess.run([OBJCOPY, '-O', 'binary', '-j', name, o, t], capture_output=True)
    try:
        b = open(t, 'rb').read()
        os.remove(t)
    except OSError:
        b = b''
    return b


_ref = {}
_ref['fns'], _ref['order'] = disasm(REF)
_ref['bytes'] = open(REF, 'rb').read()
_ref['sec'] = {s: section(REF, s) for s in ('.text', '.data', '.rdata', '.bss')}


def ref():
    return _ref


def fdiff(a, b):
    a2, b2 = norm(a), norm(b)
    if a2 == b2:
        return 0
    n = 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a2, b2, autojunk=False).get_opcodes():
        if tag != 'equal':
            n += (i2 - i1) + (j2 - j1)
    return n


def report(o):
    """(identical, total, {fn: lines}, notes)"""
    r = ref()
    b = open(o, 'rb').read()
    if b == r['bytes']:
        return True, 0, {}, ['BYTES']
    fns, order = disasm(o)
    per = {}
    for n in r['order']:
        if n not in fns:
            per[n] = 9999
        else:
            k = fdiff(r['fns'][n], fns[n])
            if k:
                per[n] = k
    notes = []
    for n in order:
        if n not in r['fns']:
            notes.append('new fn ' + n)
            per[n] = 9999
    if order != r['order'] and sorted(order) == sorted(r['order']):
        notes.append('text order differs')
    for s in ('.text', '.data', '.rdata', '.bss'):
        if section(o, s) != r['sec'][s]:
            notes.append(s + ' differs')
    return not per and not notes, sum(per.values()), per, notes


def score_text(text, flags=P98, keep=None, extra=()):
    ok, o, d = compile_src(text, flags, keep=keep, extra=extra)
    try:
        if not ok:
            return {'compile': o[:400]}
        idn, tot, per, notes = report(o)
        return {'identical': idn, 'total': tot, 'per': per, 'notes': notes}
    finally:
        cleanup(d)


def fmt(r):
    if 'compile' in r:
        return 'COMPILE ERROR ' + r['compile']
    if r['identical']:
        return 'IDENTICAL' + (' BYTES' if 'BYTES' in r['notes'] else ' (symbols differ)')
    return '%d %s %s' % (r['total'], r['per'], ' '.join(r['notes']))


if __name__ == '__main__':
    a = sys.argv[1:]
    path = a.pop(0)
    flags = P98
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
    verbose = '-v' in a
    only = None
    if verbose:
        i = a.index('-v')
        only = a[i + 1] if i + 1 < len(a) else None
    text = read_src(path)
    ok, o, d = compile_src(text, flags)
    if not ok:
        print('COMPILE ERROR', o)
        sys.exit(1)
    idn, tot, per, notes = report(o)
    print('IDENTICAL ' + ' '.join(notes) if idn else '%d %s %s' % (tot, per, ' '.join(notes)))
    if verbose and not idn:
        fns, _ = disasm(o)
        r = ref()
        for n in per:
            if only and n != only:
                continue
            if n in fns and n in r['fns']:
                print('=====', n, '(- reference, + draft)')
                for l in difflib.unified_diff(norm(r['fns'][n]), norm(fns[n]), lineterm='', n=2):
                    if not l.startswith(('---', '+++')):
                        print(l)
    cleanup(d)
