"""mode_client attempt 9: compare mode_client's profile_estimate block frequencies of two
sources (blocks matched by their labels + called functions + first statement).

python tools/wip/dehint/mc9freq.py A.c B.c [-all]
Compiles both with -fdump-tree-profile_estimate-details into build/mc4/f9a, f9b."""
import os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, mc1lib


def dump(src, tag):
    d = os.path.join(bdlib.R, 'build', 'mc4', tag)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'mode_client.c'), 'w', newline='\n').write('#line 1 "mode_client.c"\n' + mc1lib.read_src(src))
    subprocess.run([bdlib.GCC, '-c', '-O3', '-fdump-tree-profile_estimate-details', '-I' + os.path.join(bdlib.R, 'src'),
                    'mode_client.c', '-o', 'o.o'], cwd=d, capture_output=True)
    p = [f for f in os.listdir(d) if f.endswith('profile_estimate')][0]
    t = open(os.path.join(d, p)).read()
    t = t[t.index(';; Function mode_client'):]
    m = re.search(r'\n;; Function (?!mode_client )', t)
    t = t[:m.start()] if m else t
    t = t[t.index(';;   basic block 2,'):]
    out = []
    for b in re.split(r'\n(?=;;   basic block \d+,)', t):
        m = re.match(r';;   basic block (\d+), loop depth (\d+), count 0, freq (\d+)', b)
        if not m:
            continue
        body = [l.strip() for l in b.split('\n')[1:] if l.strip() and not l.startswith(';;') and not l.strip().startswith('#')]
        labs = [l[:-1] for l in body if re.fullmatch(r'\w+:', l)]
        calls = re.findall(r'(\w+) \(', ' '.join(body))
        first = next((re.sub(r'_\d+', '', l) for l in body if not re.fullmatch(r'\w+:', l)), '')
        out.append((int(m.group(1)), int(m.group(3)), ' '.join(labs), ' '.join(calls)[:60], first[:50]))
    return out


def main():
    a = sys.argv[1:]
    A, B = dump(a[0], 'f9a'), dump(a[1], 'f9b')
    def sig(r):
        return (r[2], r[3], r[4])
    bm = {}
    for r in B:
        bm.setdefault(sig(r), []).append(r)
    am = {}
    for r in A:
        am.setdefault(sig(r), []).append(r)
    for s, ra in am.items():
        rb = bm.get(s, [])
        fa = [r[1] for r in ra]
        fb = [r[1] for r in rb]
        if fa != fb or '-all' in a:
            print('A bb %s freq %s | B bb %s freq %s | %s' % ([r[0] for r in ra], fa, [r[0] for r in rb], fb, ' / '.join(s)))


if __name__ == '__main__':
    main()
