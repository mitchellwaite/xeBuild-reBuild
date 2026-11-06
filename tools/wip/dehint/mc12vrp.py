"""mode_client attempt 12: vrp1's jump threads through the mode-chain switch, in the order
they are carried out.  The order is a hash-table walk (redirection_data hash = the target
block's index, table size 13), so it follows the indices of the blocks VRP creates on the
switch edges (last_basic_block + k): one block more or fewer anywhere in mode_client before
vrp1 changes it, and with it the switch's case probabilities after threading.

python tools/wip/dehint/mc12vrp.py A.c [B.c ...]"""
import os, re, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, mc1lib


def threads(text):
    d = tempfile.mkdtemp(dir=mc1lib.BUILD, prefix='v')
    open(os.path.join(d, 'mode_client.c'), 'w', newline='\n').write('#line 1 "mode_client.c"\n' + text)
    subprocess.run([bdlib.GCC, '-c', '-O3', '-fdump-tree-vrp1-details', '-I' + os.path.join(bdlib.R, 'src'),
                    'mode_client.c', '-o', 'o.o'], cwd=d, capture_output=True)
    f = [x for x in os.listdir(d) if x.endswith('vrp1')][0]
    t = open(os.path.join(d, f), errors='replace').read()
    mc1lib.cleanup(d)
    t = t[t.index(';; Function mode_client '):]
    reg = re.findall(r'Registering jump thread: \((\d+), (\d+)\) incoming edge;(?:  \((\d+), (\d+)\) joiner;)?  \((\d+), (\d+)\) normal;', t)
    done = re.findall(r'Threaded jump (\d+) --> (\d+) to (\d+)', t)
    tgt = {}
    for r in reg:
        tgt[(r[0], r[1])] = r[5]
    return [(a, b, tgt.get((a, b), '?')) for a, b, c in done]


def main():
    for s in sys.argv[1:]:
        th = threads(mc1lib.read_src(s))
        print(os.path.basename(s), ' '.join('%s->%s(%s%%13=%d)' % (a, b, x, int(x) % 13 if x != '?' else -1) for a, b, x in th))


if __name__ == '__main__':
    main()
