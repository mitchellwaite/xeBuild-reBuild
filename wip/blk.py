"""Block order of one function: original (src/app/options.s) vs gcc -S of a C file.

python wip/blk.py <file.c> <name> [gcc flags]
Each block is summarised by the strings it references and the calls it makes.
"""
import difflib, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TC = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
src, fn = sys.argv[1:3]
flags = sys.argv[3:] or ['-O3']


def strings(lines, labre, strre):
    out, cur = {}, None
    for l in lines:
        m = re.match(labre, l)
        if m:
            cur = m.group(1)
            continue
        m = re.match(strre, l)
        if m and cur:
            out.setdefault(cur, m.group(1).replace(chr(92)+'12', chr(92)+'n').replace(chr(92)+'0', '')[:24])
    return out


def blocks(lines, fnlab, labre, strs, isend):
    s = next(i for i, l in enumerate(lines) if l.startswith(fnlab + ':'))
    res, cur = [], []
    for l in lines[s + 1:]:
        l = l.strip()
        if re.match(r'^_\w+:', l) or l.startswith('#@C') or l.startswith('.def') or isend(l):
            break
        if re.match(labre, l):
            if cur:
                res.append(cur)
            cur = []
            continue
        if not l or l.startswith('.'):
            continue
        w = l.split()
        op = w[0].lower()
        if op == 'call':
            cur.append('call ' + w[1].lstrip('_').lower())
        elif op.startswith('j'):
            cur.append(op)
            if op == 'jmp':
                res.append(cur)
                cur = []
        elif op == 'ret':
            cur.append('ret')
            res.append(cur)
            cur = []
        else:
            for m in re.finditer(r'(L_[0-9a-f]+|LC\d+|_msg_\w+|_str_\w+)', l):
                t = m.group(1)
                if t in strs:
                    cur.append('"%s"' % strs[t])
    if cur:
        res.append(cur)
    return [' '.join(b) for b in res]


orig = open(os.path.join(ROOT, 'src', 'app', 'options.s')).read().split('\n')
ostr = strings(orig, r'^(L_[0-9a-f]+|_msg_\w+|_str_\w+):', r'^\s*\.(?:string|ascii)\s+"(.*)"')
ob = blocks(orig, '_' + fn, r'^(L_[0-9a-f]+):', ostr, lambda l: False)

env = dict(os.environ, PATH=TC + os.pathsep + os.environ['PATH'])
r = subprocess.run([os.path.join(TC, 'gcc.exe'), '-S', '-masm=intel', '-fno-asynchronous-unwind-tables']
                   + flags + [src, '-o', '-'], env=env, capture_output=True, text=True)
if r.returncode:
    sys.exit(r.stderr)
mine = r.stdout.split('\n')
mstr = strings(mine, r'^(LC\d+):', r'^\s*\.(?:string|ascii)\s+"(.*)"')
mb = blocks(mine, '_' + fn, r'^(L\d+):', mstr, lambda l: l.startswith('.globl') or l.startswith('.section'))
for l in difflib.unified_diff(ob, mb, 'original', src, lineterm='', n=100):
    print(l)
