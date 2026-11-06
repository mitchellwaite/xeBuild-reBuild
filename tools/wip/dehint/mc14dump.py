"""mode_client attempt 14: gcc tree dumps of a source (vrp1-details plus the passes named),
written into OUTDIR, and a summary of mode_client at vrp1: last block index, the assert
edge splits VRP made (in order) and the thread targets.

python tools/wip/dehint/mc14dump.py A.c OUTDIR [-all]"""
import os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, mc1lib


def dump(src, out, allp=False):
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'mode_client.c'), 'w', newline='\n').write('#line 1 "mode_client.c"\n' + mc1lib.read_src(src))
    fl = ['-fdump-tree-all-details', '-fdump-rtl-bbro'] if allp else ['-fdump-tree-vrp1-details', '-fdump-tree-cfg-blocks']
    subprocess.run([bdlib.GCC, '-c', '-O3'] + fl + ['-I' + os.path.join(bdlib.R, 'src'), 'mode_client.c', '-o', 'o.o'],
                   cwd=out, capture_output=True)
    f = [x for x in os.listdir(out) if x.endswith('vrp1')][0]
    return open(os.path.join(out, f), errors='replace').read()


def summary(t):
    t = t[t.index(';; Function mode_client '):]
    nxt = t.find(';; Function ', 10)
    if nxt > 0:
        t = t[:nxt]
    first = t[:t.index('SSA form after inserting ASSERT_EXPRs')] if 'SSA form after inserting' in t else t
    bbs = [int(x) for x in re.findall(r'<bb (\d+)>', first)]
    print('max bb before asserts', max(bbs) if bbs else '?')
    aft = t[t.index('SSA form after inserting ASSERT_EXPRs'):] if 'SSA form after inserting' in t else ''
    seg = aft[:aft.find('\n\n;;')] if aft else ''
    bb2 = sorted(set(int(x) for x in re.findall(r'<bb (\d+)>', aft[:aft.find('Value ranges after VRP')]))) if aft else []
    new = [b for b in bb2 if bbs and b > max(bbs)]
    print('new blocks', new)
    reg = re.findall(r'Registering jump thread: (.*)', t)
    print('threads registered', len(reg))
    for m in re.findall(r'Threaded jump (\d+) --> (\d+) to (\d+)', t):
        print('threaded', m)


if __name__ == '__main__':
    summary(dump(sys.argv[1], sys.argv[2], '-all' in sys.argv))
