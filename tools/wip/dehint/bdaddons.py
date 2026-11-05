"""Spell the addons through xb.addons instead of past the end of xb.files, per object.

python tools/wip/dehint/bdaddons.py [-w]
Tries every spelling for each object's sites (cross product over the object's sites),
compiled as build.sh does, and compares with build/obj/<obj>.o: `same` is byte-identical.
-w writes the first identical variant of each object into src/."""
import difflib, itertools, os, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TC = os.path.join(R, 'tools', 'toolchain-4745', 'mingw32', 'bin')
os.environ['PATH'] = TC + os.pathsep + os.environ['PATH']
GCC = os.path.join(TC, 'gcc.exe')
OBJDUMP = os.path.join(TC, 'objdump.exe')
OUT = os.path.join(R, 'build', 'bd')
FLAGS = {'build': ['--param', 'builtin-expect-probability=98'],
         'options': ['--param', 'builtin-expect-probability=83']}


def forms(n):
    """natural spellings of addon n's entry, as a pointer expression"""
    return [('idx', '&xb.addons[%s]' % n), ('add', '(xb.addons + %s)' % n), ('add2', '(%s + xb.addons)' % n)]


def name(n):
    return [('idx', 'xb.addons[%s].name' % n), ('add', '(xb.addons + %s)->name' % n),
            ('addr', '(&xb.addons[%s])->name' % n)]


# object: [ (group label, [old strings], formula for the new text) ]; one spelling per group
SITES = {
    'build': [('a', ['a = &xb.files[19 + i];'], lambda: [('idx', 'a = &xb.addons[i];'), ('add', 'a = xb.addons + i;')])],
    'mode_build': [('n', ['(xb.files + xb.numPatches + XB_ADDONS)->name'], lambda: name('xb.numPatches'))],
    'mode_update': [
        ('i', ['(&xb.files[i] + XB_ADDONS)->name'], lambda: name('i')),
        ('n', ['(&xb.files[xb.numPatches] + XB_ADDONS)->name'], lambda: name('xb.numPatches')),
    ],
    'options': [
        ('i', ['(&xb.files[i] + XB_ADDONS)->name'], lambda: name('i')),
        ('n', ['(&xb.files[xb.numPatches] + XB_ADDONS)->name'], lambda: name('xb.numPatches')),
    ],
}


def read(obj):
    return open(os.path.join(R, 'src', obj + '.c'), newline='').read().replace('\r\n', '\n')


def dis(o):
    t = subprocess.run([OBJDUMP, '-d', '-r', '-M', 'intel', '--no-show-raw-insn', o],
                       capture_output=True, text=True).stdout
    out = {}
    cur = None
    for l in t.split('\n'):
        m = re.match(r'^[0-9a-f]+ <(.+)>:$', l)
        if m:
            cur = m.group(1)
            out[cur] = []
        elif cur and l.strip():
            out[cur].append(re.sub(r'^\s*[0-9a-f]+:\s*', '', l))
    return out


def compile_(obj, text):
    d = tempfile.mkdtemp(dir=OUT, prefix='a')
    o = os.path.join(d, 'o.o')
    r = subprocess.run([GCC, '-c', '-O3'] + FLAGS.get(obj, []) + ['-I' + os.path.join(R, 'src'), '-x', 'c', '-', '-o', o],
                       input=('#line 1 "%s.c"\n' % obj + text).encode(), cwd=d, capture_output=True)
    return r, o, d


def score(obj, text):
    r, o, d = compile_(obj, text)
    try:
        if r.returncode:
            return 'error ' + r.stderr.decode(errors='replace')[:200]
        ref = os.path.join(R, 'build', 'obj', obj + '.o')
        if open(o, 'rb').read() == open(ref, 'rb').read():
            return 'same'
        a, b = dis(ref), dis(o)
        per = {}
        for n in a:
            if a[n] != b.get(n):
                k = 0
                for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a[n], b.get(n, []), autojunk=False).get_opcodes():
                    if tag != 'equal':
                        k += (i2 - i1) + (j2 - j1)
                per[n] = k
        return 'diff %d %s' % (sum(per.values()), per)
    finally:
        for f in os.listdir(d):
            os.remove(os.path.join(d, f))
        os.rmdir(d)


def main():
    write = '-w' in sys.argv
    for obj, sites in SITES.items():
        base = read(obj)
        combos = list(itertools.product(*[s[2]() for s in sites]))

        def one(c):
            t = base
            for s, (lab, new) in zip(sites, c):
                for old in s[1]:
                    assert old in t, old
                    t = t.replace(old, new)
            return '+'.join(x[0] for x in c), score(obj, t), t
        with ThreadPoolExecutor(4) as ex:
            res = list(ex.map(one, combos))
        same = [r for r in res if r[1] == 'same']
        print(obj, len(same), 'of', len(res), 'identical')
        for lab, sc, _ in res:
            print('   ', lab, sc[:200])
        if write and same:
            open(os.path.join(R, 'src', obj + '.c'), 'w', newline='\n').write(same[0][2])
            print('    wrote', same[0][0])


main()
