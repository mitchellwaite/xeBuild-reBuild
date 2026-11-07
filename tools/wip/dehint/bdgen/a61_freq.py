"""Attempt 61: exp_pr's two frequencies (the SE block and the no-key log) and the function's max block
frequency, in loadBlFiles, at several tree dumps and in the RTL alignments dump.

python tools/wip/dehint/bdgen/a61_freq.py <variant.c> [-p 99] [-f fn]
  prints, per dump: max freq, SE block (the 'E' == 69 test's block), the no-key log block, and the
  r-test-after-checkBl block frequencies.  With -a also the final alignments dump's lines for blocks
  holding the no-key and SE code."""
import os, re, subprocess, sys, tempfile

R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
GCC = os.path.join(R, 'tools', 'toolchain-4745', 'mingw32', 'bin', 'gcc.exe')
env = dict(os.environ, PATH=os.path.dirname(GCC) + os.pathsep + os.environ['PATH'])
OUT = os.path.join(R, 'build', 'bd', 'a61', 'f')
os.makedirs(OUT, exist_ok=True)
PASSES = ['profile_estimate', 'fixup_cfg4', 'vrp1', 'optimized']


def dumps(text, p=99):
    d = tempfile.mkdtemp(dir=OUT)
    open(os.path.join(d, 'b.c'), 'w', newline='\n').write('#line 1 "build.c"\n' + text)
    fl = ['--param', 'builtin-expect-probability=%d' % p] if p else []
    cmd = [GCC, '-c', '-O3'] + fl + ['-I' + os.path.join(R, 'src'), 'b.c', '-o', 'b.o']
    cmd += ['-fdump-tree-%s-details-blocks' % x for x in PASSES]
    subprocess.run(cmd, cwd=d, env=env, check=True)
    return d


def func(path, fn):
    x = open(path, errors='replace').read()
    parts = [m.start() for m in re.finditer(r'^;; Function %s[ .]' % re.escape(fn), x, re.M)]
    if not parts:
        return ''
    e = x.find('\n;; Function ', parts[-1] + 10)
    return x[parts[-1]:e if e > 0 else len(x)]


def blocks(body):
    """[(bbno, freq, text)]"""
    out = []
    for m in re.finditer(r'^;;   basic block (\d+), loop depth \d+, count \d+, freq (\d+)', body, re.M):
        out.append([int(m.group(1)), int(m.group(2)), m.start()])
    res = []
    for i, (n, f, s) in enumerate(out):
        e = out[i + 1][2] if i + 1 < len(out) else len(body)
        res.append((n, f, body[s:e]))
    return res


def report(d, fn='loadBlFiles'):
    for p in PASSES:
        fs = [f for f in os.listdir(d) if f.endswith('.' + p)]
        if not fs:
            continue
        b = blocks(func(os.path.join(d, fs[0]), fn))
        if not b:
            print(p, 'no blocks'); continue
        mx = max(b, key=lambda x: x[1])
        se = [(n, f) for n, f, t in b if re.search(r'== 69\)', t)]
        nk = [(n, f) for n, f, t in b if 'rsa key not present' in t]
        sf = [(n, f) for n, f, t in b if 'signature check failed' in t]
        print('%-17s max bb%d=%d  SE %s  nokey %s  sigfail %s' % (p, mx[0], mx[1], se, nk, sf))


if __name__ == '__main__':
    a = sys.argv[1:]
    p = 99
    fn = 'loadBlFiles'
    if '-p' in a:
        i = a.index('-p'); p = int(a[i + 1]); del a[i:i + 2]
    if '-f' in a:
        i = a.index('-f'); fn = a[i + 1]; del a[i:i + 2]
    t = open(a[0], newline='').read()
    d = dumps(t, p)
    print(d)
    report(d, fn)
