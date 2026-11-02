"""ev.py SRC.c [-v FUNC] [-f "flags"] [-t TAG]: plain compile of SRC.c as mode_update.c, per-function diff vs build/obj/mode_update.o.
Prints total diff lines with padding (byte-level view) and without nops. Output under build/v/mu_p1/<tag>."""
import os, re, subprocess, sys, difflib
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
ENV = dict(os.environ, PATH=BIN + os.pathsep + os.environ.get('PATH', ''))
FLAGS = "-O3 -fno-toplevel-reorder --param builtin-expect-probability=68"
REFO = os.path.join(ROOT, 'build', 'obj', 'mode_update.o')

def tool(t): return os.path.join(BIN, t + '.exe')

def compile_(src, tag, flags=FLAGS, extra=()):
    d = os.path.join(ROOT, 'build', 'v', 'mu_p1', tag)
    os.makedirs(d, exist_ok=True)
    txt = '#line 1 "mode_update.c"\n' + open(src, newline='').read()
    o = os.path.join(d, 'o.o')
    s = os.path.join(d, 'o.s')
    # build.sh: gcc -c; here -S then as, same result
    r = subprocess.run([tool('gcc'), '-S', *flags.split(), *extra, '-I' + os.path.join(ROOT, 'src'), '-x', 'c', '-', '-o', 's.s'],
                       input=txt, env=ENV, capture_output=True, text=True, cwd=d)
    if r.returncode:
        return None, r.stderr
    r = subprocess.run([tool('as'), '--32', 's.s', '-o', 'o.o'], env=ENV, capture_output=True, text=True, cwd=d)
    return o, r.stderr

def rdata(o):
    out = subprocess.run([tool('objdump'), '-s', '-j', '.rdata', o], env=ENV, capture_output=True, text=True).stdout
    b = bytearray()
    for l in out.split('\n'):
        m = re.match(r' ([0-9a-f]+) ((?:[0-9a-f]{2,8} ){1,4})', l)
        if m:
            b += bytes.fromhex(m.group(2).replace(' ', ''))
    return bytes(b)

def funcs(o):
    rd = rdata(o)
    out = subprocess.run([tool('objdump'), '-dr', '-M', 'intel', '--no-show-raw-insn', o], env=ENV, capture_output=True, text=True).stdout
    fs = {}; cur = None; pend = None
    for l in out.split('\n'):
        m = re.match(r'^[0-9a-f]+ <([^>]+)>:', l)
        if m:
            cur = fs.setdefault(m.group(1), []); continue
        if cur is None: continue
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

NOPS = re.compile(r'^(nop|xchg ax,ax|lea esi,\[esi.*\]|lea edi,\[edi.*\]|mov esi,esi|mov edi,edi|data16.*|cs nop.*|nop .*)$')
def ndiff(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return sum(max(j2 - j1, 0) + max(i2 - i1, 0) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal')

def score(o, ref=None, only=None):
    ref = ref or funcs(REFO)
    me = funcs(o)
    r = {}
    for k in sorted(set(ref) | set(me)):
        a, b = ref.get(k, []), me.get(k, [])
        if only and k not in only: continue
        if a != b:
            r[k] = (ndiff(a, b), ndiff([x for x in a if not NOPS.match(x.split(' @')[0])], [x for x in b if not NOPS.match(x.split(' @')[0])]))
    return r

if __name__ == '__main__':
    a = sys.argv[1:]; src = a.pop(0); v = None; fl = FLAGS; tag = 'ev'
    while a:
        x = a.pop(0)
        if x == '-v': v = a.pop(0)
        elif x == '-f': fl = a.pop(0)
        elif x == '-F': fl = FLAGS + ' ' + a.pop(0)
        elif x == '-t': tag = a.pop(0)
    o, err = compile_(src, tag, fl)
    if not o:
        print(err); sys.exit(1)
    if err: print(err)
    r = score(o)
    print(r if r else 'all functions same')
    if v:
        ref = funcs(REFO); me = funcs(o)
        for l in difflib.unified_diff(ref.get(v, []), me.get(v, []), 'ref', 'mine', lineterm='', n=1):
            print(l)
