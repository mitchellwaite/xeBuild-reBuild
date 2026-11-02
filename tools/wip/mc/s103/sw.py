import sys, subprocess, concurrent.futures as cf, os
# usage: sw.py base.c prefix variants.txt ; variants lines: "LINE|OLD|NEW" (replace OLD with NEW on that line; LINE 1-based)
base, pre, vf = sys.argv[1:4]
src = open(base).read().split('\n')
vs = [l.rstrip('\n') for l in open(vf) if l.strip() and not l.startswith('#')]
def run(k):
  try: return run2(k)
  except AssertionError: return k,'skip'
def run2(k):
    parts = vs[k].split(' ;; ')
    s = list(src)
    for p in parts:
        ln, old, new = p.split('@@', 2)
        c=[i for i,x in enumerate(s) if old in x]
        assert len(c)>=1, vs[k]
        ln = c[0] if ln=='0' else int(ln)-1
        assert old in s[ln], (vs[k], s[ln])
        s[ln] = s[ln].replace(old, new, 1)
    fn = os.path.abspath('%s_%d.c' % (pre, k))
    open(fn, 'w', newline='\n').write('\n'.join(s))
    r = subprocess.run(['sh', 'f2.sh', fn], capture_output=True, text=True).stdout.strip()
    return k, r
with cf.ThreadPoolExecutor(int(os.environ.get("NT","6"))) as ex:
    for k, r in ex.map(run, range(len(vs))):
        print(r, k, vs[k], flush=True)
