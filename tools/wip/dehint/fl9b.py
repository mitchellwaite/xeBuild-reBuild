"""fl9b.py <file.c> [n]: model ivopts' releases for parseIni.

From tree_ssa_iv_optimize (LI_FROM_INNERMOST) + remove_unused_ivs -> release_defs_bitset (gcc 6.2.0): per loop, in processing
order, the unused ivs go out by ascending version, each deferred to a later sweep while another name in the set is
defined by one of its users.  The queue is spliced on the free stack at the end of the pass, so the LAST loop's LAST name
is on top.

Prints the stack top-down: position, name, loop (line), its pre-ivopts definition, and what the number is at dom3 if dom3 took it.
Dumps go to build/filelist_ini/a9/iv_<tag>/.
"""
import glob, os, re, subprocess, sys
import fllib as L
import fl9a

A9 = os.path.join(L.BD, 'a9')
os.makedirs(A9, exist_ok=True)


def dump(src, tag):
    d = os.path.join(A9, 'iv_' + tag)
    os.makedirs(d, exist_ok=True)
    for f in glob.glob(os.path.join(d, '*')):
        os.remove(f)
    inp = ('#line 1 "filelist_ini.c"\n' + open(src, newline='').read()).encode()
    subprocess.run([L.GCC, '-c', '-O3', '-fdump-tree-all', '-fdump-tree-ivopts-details', '-I' + os.path.join(L.R, 'src'), '-x', 'c', '-', '-o', 'x.o'],
                   input=inp, cwd=d, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return d


def fn(f, name='parseIni'):
    return fl9a.fn(f, name)


def stmts(q):
    """{version: (lhs text, rhs text)} and {version: set(user-defined versions)}"""
    defs, uses = {}, {}
    for ln in q.splitlines():
        m = fl9a.DEF.match(ln)
        if m:
            v = int(m.group(2))
            rhs = m.group(3)
            defs[v] = ln.strip()
            isphi = 'PHI <' in ln
            for u in re.findall(r'[\w.]*_(\d+)(?:\(D\))?', rhs):
                u = int(u)
                if not isphi:
                    uses.setdefault(u, set()).add(v)
    return defs, uses


def model(d):
    ivt = fn(glob.glob(os.path.join(d, '-.*t.ivopts'))[0])
    snk = fn(glob.glob(os.path.join(d, '-.*t.slp1'))[0])
    defs0, uses0 = stmts(snk)
    defs1, _ = stmts(re.sub(r'(?s).*?\n(?=parseIni \()', '', ivt, count=1))
    stack = []
    for part in re.split(r'(?m)^(?=Processing loop )', ivt)[1:]:
        m = re.match(r'Processing loop (\d+)(?: at \S+:(\d+))?', part)
        names = [int(x) for x in re.findall(r'(?m)^ssa name [\w.]*_(\d+)$', part.split('Uses:')[0])]
        # the set: ivs of this loop no longer defined after the pass
        rem = sorted({n for n in names if n in defs0 and n not in defs1})
        s = set(rem)
        while s:
            for j in sorted(s):
                if j not in s:
                    continue
                if any(o in s for o in uses0.get(j, ())):
                    continue
                s.discard(j)
                stack.append((j, m.group(1), m.group(2), defs0[j]))
    return stack, defs0, defs1


if __name__ == '__main__':
    src = sys.argv[1]
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    tag = os.path.basename(src).replace('.c', '')
    d = dump(src, tag)
    stack, defs0, defs1 = model(d)
    dom3 = fl9a.defs(fn(glob.glob(os.path.join(d, '-.*t.dom3'))[0]))
    split = fl9a.defs(fn(glob.glob(os.path.join(d, '-.*t.split-paths'))[0]))
    gone = set(defs0) - set(defs1)
    print('vanished at ivopts', len(gone), 'in model', len(stack), 'not in model', sorted(gone - {s[0] for s in stack})[:40])
    for i, (j, lp, line, txt) in enumerate(reversed(stack)):
        if i >= N:
            break
        now = dom3.get(j, '') if j not in split else 'taken before dom3: ' + split[j]
        print('%3d loop %-3s l%-4s %-36s -> %s' % (i, lp, line, txt[:36], now[:50]))
