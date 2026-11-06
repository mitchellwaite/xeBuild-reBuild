"""mode_client attempt 16: GIMPLE block frequencies (pass dump with -blocks-details) of the
blocks in mode_client that call one of the given functions or hold one of the given labels.

python tools/wip/dehint/mc16freq.py A.c PASS name[,name...]   (PASS e.g. profile_estimate, vrp1)"""
import os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, mc1lib


def freqs(t, ps, names):
    d = tempfile.mkdtemp(dir=mc1lib.BUILD, prefix='k')
    open(os.path.join(d, 'mode_client.c'), 'w', newline='\n').write(t)
    subprocess.run([bdlib.GCC, '-c', '-O3', '-fdump-tree-%s-blocks-details' % ps,
                    '-I' + os.path.join(bdlib.R, 'src'), 'mode_client.c', '-o', 'o.o'], cwd=d, capture_output=True)
    f = [x for x in os.listdir(d) if x.endswith(ps)][0]
    s = open(os.path.join(d, f)).read()
    mc1lib.cleanup(d)
    s = s[s.index(';; Function mode_client'):]
    if ';; Function ' in s[10:]:
        s = s[:s.index(';; Function ', 10)]
    out = []
    for b in re.split(r'\n(?=;;   basic block)', s):
        m = re.search(r'basic block (\d+), loop depth \d+, count \d+, +freq (\d+)', b)
        hit = [n for n in names if n + ' (' in b or ('\n' + n + ':') in b]
        if m and hit:
            out.append((int(m.group(1)), int(m.group(2)), hit))
    return out


if __name__ == '__main__':
    for bb, f, hit in freqs(mc1lib.read_src(sys.argv[1]), sys.argv[2], sys.argv[3].split(',')):
        print('bb', bb, 'freq', f, hit)
