"""Diagnostic: hinted src/net.c, verbose hint window. For N in sweep, -O3 --param builtin-expect-probability=N:
netRecvVerbose lines (asm kept), plus alignment directives inside the function compared with N=65.
python tools/wip/dehint/nrwin.py"""
import os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
FNCMP = os.path.join(ROOT, 'tools', 're', 'fncmp.py')
out = os.path.join(ROOT, 'build', 'nr', 'win')
os.makedirs(out, exist_ok=True)
env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
src = os.path.join(ROOT, 'src', 'net.c')


def fn(s, sym):
    i = s.index(sym + ':')
    j = s.find('.def', i)
    return s[i:j]


base = None
res = {}
for N in [65] + list(range(50, 72)):
    asm = os.path.join(out, 'n%d.s' % N)
    subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-fno-asynchronous-unwind-tables', '-O3', '-I', os.path.join(ROOT, 'src'),
                    '--param', 'builtin-expect-probability=%d' % N, src, '-o', asm], env=env, check=True)
    s = open(asm).read()
    r = subprocess.run([sys.executable, FNCMP, src, 'netRecvVerbose'], capture_output=True, text=True, cwd=ROOT, env=dict(os.environ, FNCMP_ASM=asm))
    o = r.stdout.strip()
    n = 0 if o == 'MATCH' else len([l for l in o.split('\n') if re.match(r'^[-+][^-+]', l)])
    al = [l.strip() for l in fn(s, '_netRecvVerbose').split('\n') if 'p2align' in l or l.endswith(':')]
    alseq = []
    last = ''
    pos = 0
    for l in fn(s, '_netRecvVerbose').split('\n'):
        l = l.strip()
        if not l:
            continue
        if l.startswith('.p2align'):
            alseq.append((pos, l))
        elif not l.endswith(':') and not l.startswith('.'):
            pos += 1
    if base is None:
        base = alseq
    print(N, 'lines', n, 'align same as 65:', alseq == base, '' if alseq == base else [a for a in alseq if a not in base] + ['-'] + [a for a in base if a not in alseq])
