"""mode_client attempt 12: RTL (bbro) frequency and trace position of the blocks that hold
named labels (rtl_dce numbering = the numbering of bbro's trace lines).

python tools/wip/dehint/mc12keys.py A.c [B.c ...] [-l c9,c11,c7,p1,c10,c12]"""
import os, re, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, mc1lib

LABS = ['c9', 'c11', 'c7', 'p1', 'c10', 'c12', 'i1', 'cdef', 'c1', 'c2', 'c3', 't4', 't5']


def fn_part(t):
    t = t[t.index(';; Function mode_client '):]
    m = re.search(r'\n;; Function ', t[10:])
    return t[:m.start() + 10] if m else t


def keys(text, labs=LABS):
    d = tempfile.mkdtemp(dir=mc1lib.BUILD, prefix='k')
    open(os.path.join(d, 'mode_client.c'), 'w', newline='\n').write('#line 1 "mode_client.c"\n' + text)
    subprocess.run([bdlib.GCC, '-c', '-O3', '-fdump-rtl-bbro-details', '-fdump-rtl-rtl_dce',
                    '-I' + os.path.join(bdlib.R, 'src'), 'mode_client.c', '-o', 'o.o'], cwd=d, capture_output=True)
    fs = os.listdir(d)
    dce = fn_part(open(os.path.join(d, [f for f in fs if f.endswith('rtl_dce')][0])).read())
    bb = fn_part(open(os.path.join(d, [f for f in fs if f.endswith('bbro')][0])).read())
    mc1lib.cleanup(d)
    l2b = {}
    for m in re.finditer(r'\(code_label \d+ \d+ \d+ (\d+) \d+ \("(\w+)"\)', dce):
        l2b[m.group(2)] = int(m.group(1))
    freq, tr = {}, {}
    for m in re.finditer(r'Trace (\d+) \(round \d\):(.*)', bb):
        for b, f in re.findall(r'(\d+) \[(\d+)\]', m.group(2)):
            freq[int(b)] = int(f)
            tr[int(b)] = int(m.group(1))
    fo = [int(x) for x in re.search(r'Final order:\n(.*)', bb).group(1).split()]
    out = {}
    for l in labs:
        b = l2b.get(l)
        out[l] = (b, freq.get(b), tr.get(b), fo.index(b) if b in fo else None)
    return out


def main():
    a = sys.argv[1:]
    labs = LABS
    if '-l' in a:
        labs = a[a.index('-l') + 1].split(',')
        a = a[:a.index('-l')] + a[a.index('-l') + 2:]
    for s in a:
        k = keys(mc1lib.read_src(s), labs)
        print(os.path.basename(s), ' '.join('%s=%s[%s]T%s@%s' % ((l,) + k[l]) for l in labs))


if __name__ == '__main__':
    main()
