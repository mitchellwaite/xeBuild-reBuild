"""Attempt 51: predictions and block frequencies of one function in a variant's profile_estimate dump.
python tools/wip/dehint/bdgen/a51_fpred.py <variant.c> <function>   (e.g. a variant written by a46run.py -k)"""
import os, re, subprocess, sys, tempfile

R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
GCC = os.path.join(R, 'tools', 'toolchain-4745', 'mingw32', 'bin', 'gcc.exe')
env = dict(os.environ, PATH=os.path.dirname(GCC) + os.pathsep + os.environ['PATH'])
OUT = os.path.join(R, 'build', 'bd', 'a51')
os.makedirs(OUT, exist_ok=True)


def dump(text, fn):
    d = tempfile.mkdtemp(dir=OUT)
    open(os.path.join(d, 'b.c'), 'w', newline='\n').write('#line 1 "build.c"\n' + text)
    subprocess.run([GCC, '-c', '-O3', '--param', 'builtin-expect-probability=99', '-I' + os.path.join(R, 'src'),
                    'b.c', '-o', 'b.o', '-fdump-tree-profile_estimate-details-blocks'], cwd=d, env=env, check=True)
    f = [f for f in os.listdir(d) if f.endswith('profile_estimate')][0]
    x = open(os.path.join(d, f), errors='replace').read()
    parts = [m.start() for m in re.finditer(r'^;; Function %s[ .]' % re.escape(fn), x, re.M)]
    e = x.find('\n;; Function ', parts[-1] + 10)
    return x[parts[0]:e if e > 0 else len(x)]


if __name__ == '__main__':
    t = open(sys.argv[1], newline='').read()
    for l in dump(t, sys.argv[2]).splitlines():
        if ('heuristics' in l and 'DS' not in l and 'first' not in l) or l.startswith('Predictions') \
           or re.match(r';;   basic block', l) or re.match(r'  (if|switch|.*= \w+ \(|return)', l):
            print(l)
