"""Jump targets and offsets of one function: gcc -c of a C file vs xeBuild.exe.

python wip/jcmp.py <file.c> <name> [gcc flags]
fncmp compares every label as `l`, so a jump to the wrong (tail-merged)
block passes it.  This assembles the function and diffs instruction offsets,
mnemonics and internal jump targets against the exe (calls, data addresses
and jumps out of the function are masked).  Prints JMATCH or a diff; the
remaining noise is relocation addends (`ds:0x0`, small immediates).
"""
import os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
sys.path.insert(0, os.path.join(ROOT, 're'))
from split import SYMBOLS
from ddfix import Image
from units import units
env = dict(os.environ, PATH=BIN + os.pathsep + os.environ.get('PATH', ''))
src, fn = sys.argv[1:3]
flags = sys.argv[3:] or ['-O3']
addr = next(a for a, s in SYMBOLS.items() if s == '_' + fn)
size = dict(f for _, fs in units(Image(os.path.join(ROOT, 'xeBuild.exe'))) for f in fs)[addr]
# one .o per process, so parallel runs don't overwrite each other's
tmp = os.path.join(ROOT, 'build', 'jcmp.%d.o' % os.getpid())
r = subprocess.run([os.path.join(BIN, 'gcc.exe'), '-c', '-fno-asynchronous-unwind-tables', '-I', os.path.dirname(src)] + flags + [src, '-o', tmp], env=env, capture_output=True, text=True)
if r.returncode:
    sys.exit(r.stderr)


def dis(path, start=None, stop=None, sym=None):
    args = [os.path.join(BIN, 'objdump.exe'), '-d', '-M', 'intel', '--no-show-raw-insn']
    if start is not None:
        args += ['--start-address=0x%x' % start, '--stop-address=0x%x' % stop]
    out = subprocess.run(args + [path], env=env, capture_output=True, text=True).stdout
    lines = out.split('\n')
    if sym:
        i = next(k for k, l in enumerate(lines) if l.endswith('<_%s>:' % sym))
        res = []
        for l in lines[i + 1:]:
            if re.match(r'^[0-9a-f]+ <', l) or not l.strip():
                if res:
                    break
                continue
            res.append(l)
        lines = res
    out = []
    base = None
    for l in lines:
        m = re.match(r'^\s*([0-9a-f]+):\s+(.*)$', l)
        if not m:
            continue
        off = int(m.group(1), 16)
        if base is None:
            base = off
        ins = m.group(2).strip()
        mm = re.match(r'^(j\w+|loop\w*)\s+(?:0x)?([0-9a-f]+)', ins)
        if mm:
            t = int(mm.group(2), 16) - base
            ins = '%s +%x' % (mm.group(1), t) if 0 <= t < size and t != off - base + 1 else mm.group(1) + ' EXT'
        elif ins.startswith('call'):
            ins = 'call'
        else:
            ins = re.sub(r'0x[0-9a-f]{3,}', 'A', ins)
            ins = re.sub(r'ds:0x[0-9a-f]+', 'ds:A', ins)
        out.append('%04x %s' % (off - base, ins))
    return out


a = dis(os.path.join(ROOT, 'xeBuild.exe'), addr, addr + size)
b = dis(tmp, sym=fn)
os.remove(tmp)
# trim trailing padding
def trim(x):
    while x and re.search(r' (nop|lea\s+e[sd]i,\[e[sd]i|xchg|mov\s+esi,esi|mov\s+edi,edi|lea\s+esi,\[esi|lea\s+edi,\[edi|\(bad\)|add\s+BYTE PTR \[eax\],al)', x[-1]):
        x.pop()
    return x
a, b = trim(a), trim(b)
import difflib
# the .o's relocated fields hold addends where the exe has addresses (A)
if len(a) == len(b):
    b = [x if re.fullmatch(re.escape(x).replace('A', '(?:A|(?:0x)?[0-9a-f]+)'), y) else y for x, y in zip(a, b)]
d = list(difflib.unified_diff(a, b, 'orig', 'ours', lineterm='', n=1))
print('JMATCH' if not d else '\n'.join(d))
