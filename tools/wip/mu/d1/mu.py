"""mu.py: compile + compare helpers for mode_update de-hinting (attempt d1).

CLI:  python mu.py SRC.c [-f "flags"] [-t TAG] [-v FUNC] [-d]
  compiles SRC.c as build.sh does, prints whole-object section compare and the
  per-function diff against build/obj/mode_update.o.  -v FUNC prints the diff,
  -d also writes bbro + profile_estimate dumps to build/v/mu_d1/TAG.
Flags default to FLAGS (no param, no toplevel-reorder).
"""
import difflib
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
ENV = dict(os.environ, PATH=BIN + os.pathsep + os.environ.get('PATH', ''))
FLAGS = '-O3'
REFO = os.path.join(ROOT, 'build', 'obj', 'mode_update.o')
OUT = os.path.join(ROOT, 'build', 'v', 'mu_d1')
SECS = ['.text', '.data', '.bss', '.rdata', '.rdata$zzz', '.eh_frame']


def tool(t):
    return os.path.join(BIN, t + '.exe')


def compile_text(txt, tag, flags=FLAGS, dumps=False):
    d = os.path.join(OUT, tag)
    os.makedirs(d, exist_ok=True)
    src = '#line 1 "mode_update.c"\n' + txt
    extra = ['-fdump-rtl-bbro-details', '-fdump-tree-profile_estimate-blocks-details'] if dumps else []
    if dumps:
        with open(os.path.join(d, 'm.c'), 'w', newline='\n') as f:
            f.write(src)
        r = subprocess.run([tool('gcc'), '-S', *flags.split(), *extra, '-I' + os.path.join(ROOT, 'src'), 'm.c', '-o', 'm.s'],
                           env=ENV, capture_output=True, text=True, cwd=d)
        if r.returncode:
            return None, r.stderr
        r = subprocess.run([tool('as'), '--32', 'm.s', '-o', 'o.o'], env=ENV, capture_output=True, text=True, cwd=d)
    else:
        r = subprocess.run([tool('gcc'), '-c', *flags.split(), '-I' + os.path.join(ROOT, 'src'), '-x', 'c', '-', '-o', 'o.o'],
                           input=src, env=ENV, capture_output=True, text=True, cwd=d)
    if r.returncode:
        return None, r.stderr
    return os.path.join(d, 'o.o'), r.stderr


def objdump(o, *a):
    return subprocess.run([tool('objdump'), *a, o], env=ENV, capture_output=True, text=True).stdout


def rdata(o):
    b = bytearray()
    for l in objdump(o, '-s', '-j', '.rdata').split('\n'):
        m = re.match(r' ([0-9a-f]+) ((?:[0-9a-f]{2,8} ){1,4})', l)
        if m:
            b += bytes.fromhex(m.group(2).replace(' ', ''))
    return bytes(b)


def sec_cmp(o, ref=REFO):
    """{section: same?} + relocs."""
    r = {}
    for s in SECS:
        a = objdump(o, '-s', '-j', s).split('\n')[3:]
        b = objdump(ref, '-s', '-j', s).split('\n')[3:]
        r[s] = a == b
    a = objdump(o, '-r').split('\n')[3:]
    b = objdump(ref, '-r').split('\n')[3:]
    r['relocs'] = a == b
    return r


def funcs(o):
    rd = rdata(o)
    fs = {}
    cur = None
    for l in objdump(o, '-dr', '-M', 'intel', '--no-show-raw-insn').split('\n'):
        m = re.match(r'^[0-9a-f]+ <([^>]+)>:', l)
        if m:
            cur = fs.setdefault(m.group(1), [])
            continue
        if cur is None:
            continue
        m = re.match(r'\s+[0-9a-f]+: (DIR32|DISP32|REL32)\s+(\S+)', l)
        if m:
            sym = m.group(2)
            mm = re.match(r'\.rdata(?:\+0x([0-9a-f]+))?$', sym)
            if mm:
                off = int(mm.group(1) or '0', 16)
                e = rd.find(b'\0', off)
                sym = '"' + rd[off:min(e, off + 40)].decode('latin1') + '"'
            cur[-1] = cur[-1] + ' @' + sym
            continue
        m = re.match(r'\s+([0-9a-f]+):\s+(.*)$', l)
        if m:
            t = re.sub(r'\s+', ' ', m.group(2)).strip()
            t = re.sub(r'^(j\w+|call) .*$', r'\1', t)
            t = re.sub(r'0x[0-9a-f]+', 'X', t) if '@' in t or 'ds:' in t else t
            cur.append(t)
    return fs


_ref = None


def ref():
    global _ref
    if _ref is None:
        _ref = funcs(REFO)
    return _ref


NOPS = re.compile(r'^(nop|xchg ax,ax|lea esi,\[esi.*\]|lea edi,\[edi.*\]|mov esi,esi|mov edi,edi|data16.*|cs nop.*|nop .*)$')


def ndiff(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return sum(max(j2 - j1, 0) + max(i2 - i1, 0) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal')


def strip_nops(a):
    return [x for x in a if not NOPS.match(x.split(' @')[0])]


def score(o):
    """{func: (diff, diff-without-nops)} for functions that differ."""
    R = ref()
    me = funcs(o)
    r = {}
    for k in sorted(set(R) | set(me)):
        a, b = R.get(k, []), me.get(k, [])
        if a != b:
            r[k] = (ndiff(a, b), ndiff(strip_nops(a), strip_nops(b)))
    return r


def total(sc):
    return sum(v[0] for v in sc.values())


def order_key(o, fn):
    return funcs(o).get(fn, [])


def run_text(txt, tag, flags=FLAGS, dumps=False):
    """-> (total, score-dict, sections-all-same) or (None, err, False)."""
    o, err = compile_text(txt, tag, flags, dumps)
    if not o:
        return None, err, False
    sc = score(o)
    same = all(sec_cmp(o).values()) if not sc else None
    if same is None:
        same = False
    return total(sc), sc, same


if __name__ == '__main__':
    a = sys.argv[1:]
    src = a.pop(0)
    fl = FLAGS
    tag = 'ev'
    v = None
    dumps = False
    while a:
        x = a.pop(0)
        if x == '-f':
            fl = a.pop(0)
        elif x == '-t':
            tag = a.pop(0)
        elif x == '-v':
            v = a.pop(0)
        elif x == '-d':
            dumps = True
    txt = open(src, newline='').read()
    o, err = compile_text(txt, tag, fl, dumps)
    if not o:
        print(err)
        sys.exit(1)
    if err.strip():
        print(err[:1500])
    sc = score(o)
    print('funcs:', sc if sc else 'all same', 'total', total(sc))
    print('sections:', ' '.join(k + ('=same' if s else '=DIFF') for k, s in sec_cmp(o).items()))
    if v:
        for l in difflib.unified_diff(ref().get(v, []), funcs(o).get(v, []), 'ref', 'mine', lineterm='', n=1):
            print(l)
