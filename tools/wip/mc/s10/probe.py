"""which bbro blocks does a tree-edge override move?  python probe.py base.json edge=p ..."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run
ROOT = run.ROOT
def freqs(slot):
    t = open(ROOT + r'\build\mcsp\slot%s\m.c.274r.bbro' % slot).read()
    s = t.index(';; Function mode_client '); t = t[s:t.find('\n;; Function ', s + 1)]
    t = t[t.index('Trace 1 ('):]
    return {int(a): int(b) for a, b in re.findall(r'(\d+) \[(\d+)\]', t.split('\n\n')[0])}
if __name__ == '__main__':
    base = json.load(open(sys.argv[1]))
    run.run('p0', base); f0 = freqs('p0')
    for a in sys.argv[2:]:
        x = dict(base); k, v = a.split('='); x[k] = float(v)
        f, inv, pre, _ = run.run('p1', x); f1 = freqs('p1')
        d = {b: (f0.get(b), f1.get(b)) for b in set(f0) | set(f1) if f0.get(b) != f1.get(b)}
        print(a, 'fncmp', f, 'inv', inv, 'pre', pre, 'changed:', ' '.join('%d:%s>%s' % (b, *d[b]) for b in sorted(d)))
