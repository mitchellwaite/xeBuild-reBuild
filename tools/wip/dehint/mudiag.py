"""Diagnostics only (uses expect + param, never a candidate): which probability on the
hex arm's validateString test would match with the single x test?"""
import concurrent.futures as cf, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
s = open(os.path.join(ROOT, 'build', 'mu32', 'plain.c'), newline='').read()
t = s.replace("if(validateString(&dat[2]))\n\t\t\treturn myatox32(&dat[2], defValue);",
              "if(__builtin_expect(validateString(&dat[2]),1))\n\t\t\treturn myatox32(&dat[2], defValue);")
assert s != t
p = os.path.join(ROOT, 'build', 'mu32', 'x', 'v.c')
open(p, 'w', newline='\n').write(t)


def run(n):
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 're', 'fncmp.py'), p, 'myatou32', '-O3',
                        '-I' + os.path.join(ROOT, 'src'), '--param', 'builtin-expect-probability=%d' % n],
                       capture_output=True, text=True, cwd=ROOT)
    o = r.stdout + r.stderr
    return n, 0 if o.strip() == 'MATCH' else len([l for l in o.split('\n') if re.match(r'^[-+][^-+]', l)])


with cf.ThreadPoolExecutor(4) as ex:
    print(' | '.join('%d %d' % x for x in ex.map(run, range(20, 80))))
