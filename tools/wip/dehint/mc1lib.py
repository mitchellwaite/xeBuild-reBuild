"""mode_client de-hinting (attempt 1): compile a source text as build.sh does and compare
the object with build/mc/reference.o (a copy of a matching build/obj/mode_client.o).

python tools/wip/dehint/mc1lib.py <file.c> [-np] [-v [fn]]
  -np  plain -O3 (no --param builtin-expect-probability=50)
Report: IDENTICAL when the whole .o is byte-identical (BYTES) or when .text disassembly,
.rdata, .data and relocations all match; else differing lines per function and sections."""
import difflib, os, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib

R = bdlib.R
BUILD = os.path.join(R, 'build', 'mc')
REF = os.path.join(BUILD, 'reference.o')
SRC = os.path.join(R, 'src', 'mode_client.c')
os.makedirs(BUILD, exist_ok=True)
P50 = ['--param', 'builtin-expect-probability=50']
SECS = ('.text', '.data', '.rdata', '.bss')
read_src = bdlib.read_src
cleanup = bdlib.cleanup


def relocs(o):
    t = subprocess.run([bdlib.OBJDUMP, '-r', o], capture_output=True, text=True).stdout
    return [l for l in t.split('\n') if l and not l.startswith(('In archive', o))]


_ref = {'bytes': open(REF, 'rb').read()}
_ref['fns'], _ref['order'] = bdlib.disasm(REF)
_ref['sec'] = {s: bdlib.section(REF, s) for s in SECS}
_ref['rel'] = relocs(REF)


def compile_src(text, flags=P50, keep=None, extra=()):
    d = tempfile.mkdtemp(dir=BUILD, prefix='t')
    o = keep or os.path.join(d, 'o.o')
    src = '#line 1 "mode_client.c"\n' + text
    r = subprocess.run([bdlib.GCC, '-c', '-O3'] + list(flags) + list(extra) +
                       ['-I' + os.path.join(R, 'src'), '-x', 'c', '-', '-o', o],
                       input=src.encode(), cwd=d, capture_output=True)
    if r.returncode:
        return False, r.stderr.decode(errors='replace'), d
    return True, o, d


def report(o):
    r = _ref
    if open(o, 'rb').read() == r['bytes']:
        return True, 0, {}, ['BYTES']
    fns, order = bdlib.disasm(o)
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
        if bdlib.section(o, s) != r['sec'][s]:
            notes.append(s + ' differs')
    if relocs(o) != r['rel']:
        notes.append('relocs differ')
    return not per and not notes, sum(per.values()), per, notes


def score_text(text, flags=P50, extra=()):
    ok, o, d = compile_src(text, flags, extra=extra)
    try:
        if not ok:
            return {'compile': o[-600:]}
        idn, tot, per, notes = report(o)
        return {'identical': idn, 'total': tot, 'per': per, 'notes': notes}
    finally:
        cleanup(d)


def fmt(s):
    if 'compile' in s:
        return 'COMPILE ' + s['compile'].strip().split('\n')[-1][:160]
    if s['identical']:
        return 'IDENTICAL ' + ' '.join(s['notes'])
    return '%d %s %s' % (s['total'], s['per'], ' '.join(s['notes']))


def vdiff(text, flags=P50, only=None):
    ok, o, d = compile_src(text, flags)
    if not ok:
        print('COMPILE ERROR', o)
        return
    idn, tot, per, notes = report(o)
    print(fmt({'identical': idn, 'total': tot, 'per': per, 'notes': notes}))
    fns, _ = bdlib.disasm(o)
    for n in per:
        if only and n != only:
            continue
        a, b = _ref['fns'].get(n, []), fns.get(n, [])
        for l in difflib.unified_diff(a, b, 'ref', 'new', n=2, lineterm=''):
            print(l)
    cleanup(d)


if __name__ == '__main__':
    a = sys.argv[1:]
    flags = [] if '-np' in a else P50
    v = '-v' in a
    only = None
    if v:
        k = a.index('-v')
        if k + 1 < len(a) and not a[k + 1].startswith('-'):
            only = a[k + 1]
    text = read_src(a[0])
    if v:
        vdiff(text, flags, only)
    else:
        print(fmt(score_text(text, flags)))
