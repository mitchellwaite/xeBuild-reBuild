"""Attempt 4: frequency of applyIniOptions' xellbutton call block at profile_estimate.

python tools/wip/dehint/opfq.py file.c [pattern]   (default pattern: getIniValue ("xellbutton"))
Prints the block's frequency and the predictions on its predecessor edges, and the frequency
of every block in applyIniOptions that holds the pattern.  Target (notes/options.md, attempt
3): call block in ~[169, 173.6] so the inlined header's `!s` is 37."""
import os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, bdlib


def dump(text, flags=optlib.P83):
    d = tempfile.mkdtemp(dir=optlib.BUILD, prefix='f')
    src = os.path.join(d, 'a.c')
    open(src, 'w', newline='\n').write(text)
    r = subprocess.run([bdlib.GCC, '-c', '-O3'] + list(flags) +
                       ['-fno-ipa-profile', '-fno-reorder-functions',
                        '-fdump-tree-profile_estimate-blocks-details',
                        '-I' + os.path.join(optlib.R, 'src'), 'a.c', '-o', 'a.o'],
                       cwd=d, capture_output=True)
    if r.returncode:
        print(r.stderr.decode(errors='replace')[:2000])
        return None, d
    f = [x for x in os.listdir(d) if 'profile_estimate' in x][0]
    return open(os.path.join(d, f)).read(), d


def fn(dumptext, name):
    i = dumptext.rfind(';; Function %s ' % name)
    j = dumptext.find('\n;; Function ', i + 1)
    return dumptext[i:j if j > 0 else None]


def blocks(body):
    """[(bb, freq, text)]"""
    out = []
    for m in re.finditer(r'<bb (\d+)>:?\s*\[([0-9.]+)%\]|;;   basic block (\d+), loop depth \d+, count \d+, freq (\d+)', body):
        pass
    parts = re.split(r'(?=;;   basic block \d+, loop depth)', body)
    for p in parts:
        m = re.match(r';;   basic block (\d+), loop depth \d+, count \d+, freq (\d+)', p)
        if m:
            out.append((int(m.group(1)), int(m.group(2)), p))
    return out


def main():
    a = sys.argv[1:]
    text = open(a[0]).read()
    pat = a[1] if len(a) > 1 else 'getIniValue ("xellbutton")'
    dt, d = dump(text)
    if dt is None:
        return
    body = fn(dt, 'applyIniOptions')
    for bb, fr, p in blocks(body):
        if pat in p:
            print('bb', bb, 'freq', fr)
            for l in p.split('\n'):
                if 'pred:' in l or 'succ:' in l:
                    print('   ', l.strip())
    # predictions lines mentioning edges
    if '-p' in a:
        for l in body.split('\n'):
            if 'heuristics' in l or 'combined' in l or 'Predictions for' in l:
                print(l)
    bdlib.cleanup(d)


if __name__ == '__main__':
    main()
