#!/usr/bin/env python3
"""mode_client attempt 17, second part: what the inliner makes of a getArgs spelling.

For a file whose arms call getArgs, the inline growth gcc estimates for each getArgs call
(read from -fdump-ipa-inline-details with the auto limit raised to 100 so every edge is
considered; a measuring device only).  gcc inlines a call of a function not declared
inline when the growth is under 40 (--param max-inline-insns-auto).

python tools/wip/dehint/mc17gs.py FILE.c ..        (files written by mc17ga.py -o or by hand)"""
import os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib
import mc17lib as L


def growths(text):
    """[(frequency, growth, callee)] for the getArgs edges, and ipa-cp's clone decision"""
    d = tempfile.mkdtemp(dir=L.BUILD, prefix='g')
    open(os.path.join(d, 'mode_client.c'), 'w', newline='\n').write('#line 1 "mode_client.c"\n' + text)
    subprocess.run([bdlib.GCC, '-c', '-O3', '--param', 'max-inline-insns-auto=100', '-fdump-ipa-inline-details',
                    '-fdump-ipa-cp-details', '-I' + os.path.join(L.R, 'src'), 'mode_client.c', '-o', 'o.o'],
                   cwd=d, capture_output=True)
    out = []
    try:
        t = open(os.path.join(d, [f for f in os.listdir(d) if f.endswith('i.inline')][0]), encoding='latin1').read()
        for m in re.finditer(r'Considering (getArgs[\w.]*)/\d+ with \d+ size\n.*\n Estimated badness is [-\d.e]+, frequency ([\d.]+)\.\n.*\n\s+size growth (-?\d+), time (-?\d+)', t):
            out.append((float(m.group(2)), int(m.group(3)), m.group(1)))
        c = open(os.path.join(d, [f for f in os.listdir(d) if f.endswith('i.cp')][0]), encoding='latin1').read()
        ev = re.findall(r'good_cloning_opportunity_p \(time: (\d+), size: (\d+), freq_sum: (\d+)\) -> evaluation: (\d+)', c[:c.find('Evaluating opportunities for clientEraseBlock')])
        clone = 'Creating a specialized node of getArgs' in c
    finally:
        L.cleanup(d)
    return sorted(set(out), reverse=True), clone, max([int(e[3]) for e in ev] or [0])


if __name__ == '__main__':
    for f in sys.argv[1:]:
        g, clone, ev = growths(L.read_src(f))
        print('%s: %s  clone=%s (best evaluation %d, threshold 500)' % (
            os.path.basename(f), ' '.join('%g:%d' % (fr, gr) for fr, gr, _ in g), clone, ev))
