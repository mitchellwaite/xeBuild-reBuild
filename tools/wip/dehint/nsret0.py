"""python tools/wip/dehint/nsret0.py <src.c> [gcc flags]: netSendFile's shared return-0 block at final's compute_alignments.

Finds the block the name test jumps to, in the jump2/bbro order, and prints its pred edges and the alignment test:
aligned when branch > 4 * fallthru (align-loop-iterations 4).
"""
import os, re, subprocess, sys, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')


def run(src, flags):
    src = os.path.abspath(src)
    os.makedirs(os.path.join(ROOT, 'build', 'ns', 'probe'), exist_ok=True)
    d = tempfile.mkdtemp(dir=os.path.join(ROOT, 'build', 'ns', 'probe'))
    env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
    subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-fno-asynchronous-unwind-tables', '-O3',
                    '-I', os.path.join(ROOT, 'src'), '-fdump-rtl-bbro-blocks-details'] + flags + [src, '-o', 'a.s'],
                   cwd=d, env=env, check=True)
    t = open(os.path.join(d, next(x for x in os.listdir(d) if x.endswith('r.bbro')))).read()
    t = t[t.index(';; Function netSendFile ('):]
    j = t.find('\n;; Function ', 10)
    t = t[:j] if j > 0 else t
    i = t.rfind('(note 1 0')
    body = t[i:]
    # blocks: header lines
    blocks = re.split(r'(?m)^(?=;; basic block \d+, loop depth)', body)[1:]
    info = {}
    order = []
    for b in blocks:
        m = re.match(r';; basic block (\d+), loop depth \d+(?:, count \d+)?, freq (\d+)', b)
        if not m:
            m = re.match(r';; basic block (\d+), loop depth \d+', b)
        n = int(m.group(1))
        order.append(n)
        fq = re.search(r'freq[: ]+(\d+)', b.split('\n')[0])
        prds = []
        for l in re.findall(r';;\s+(?:pred:)?\s+(\d+|ENTRY) \[([\d.]+)%\]\s*\(([^)]*)\)', b.split('(note')[0]):
            prds.append(l)
        info[n] = (int(fq.group(1)) if fq else None, prds, b)
    shutil.rmtree(d)
    return order, info, t


def main():
    order, info, t = run(sys.argv[1], sys.argv[2:])
    print('order', order)
    for n in order:
        fq, prds, b = info[n]
        print(n, fq, prds, 'xor' if re.search(r'const_int 0 \[0\]\)\)', b[:400]) else '')


if __name__ == '__main__':
    main()
