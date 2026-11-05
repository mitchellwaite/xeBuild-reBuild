"""python tools/wip/dehint/bdpasses.py file.c fn regex [outdir]: count regex in fn's body after each tree pass and print where the count changes.

Dumps every tree pass with -details-blocks.  With outdir the dumps are kept (one fresh directory per run), otherwise they
go to a temporary directory under build/bd.  Handy for asking which pass makes a copy of a block."""
import os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib


def fnbody(path, fn):
    out, on = [], False
    for l in open(path, errors='replace'):
        if l.startswith(';; Function '):
            on = l.split()[2] == fn
            seen = False
        elif on:
            if l.startswith(fn + ' ('):
                seen = True
            if seen:
                out.append(l)
    return out


def main():
    f, fn, rx = sys.argv[1:4]
    d = sys.argv[4] if len(sys.argv) > 4 else tempfile.mkdtemp(dir=bdlib.BUILD, prefix='p')
    os.makedirs(d, exist_ok=True)
    src = '#line 1 "build.c"\n' + bdlib.read_src(f)
    subprocess.run([bdlib.GCC, '-c', '-O3'] + bdlib.P98 + ['-fdump-tree-all-details-blocks', '-I' + os.path.join(bdlib.R, 'src'),
                                                      '-x', 'c', '-', '-o', 'o.o'], input=src.encode(), cwd=d, check=True)
    names = [n for n in os.listdir(d) if re.search(r'\.t\d+\.', 'x' + n) or re.search(r'\.\d+t\.', n)]
    names.sort(key=lambda n: int(re.search(r'\.(\d+)t\.', n).group(1)))
    prev = None
    for n in names:
        c = sum(1 for l in fnbody(os.path.join(d, n), fn) if re.search(rx, l))
        if c != prev:
            print(n.split('.', 1)[1], c)
        prev = c
    print('dumps in', d)


if __name__ == '__main__':
    main()
