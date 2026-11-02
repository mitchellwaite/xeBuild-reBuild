import json, sys, os, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lev, cm, tt
B = ['2:1038:ins/next/53', '3:53:push/53/0', '4:55:ins/this/77', '4:55:ins/this/79']
rs = [json.loads(l) for l in open(sys.argv[1])]
mv = [r for r in rs if 'sig' in r and r['sig'] != B and r['inv'] + 5 * len(r['miss']) <= int(sys.argv[3])]
print(len(mv), flush=True)
def f(r):
    p = os.path.join(lev.D, 'cc%d.c' % tt.tid()); open(p, 'w', newline='\n').write(lev.make(*r['c']))
    r['cm'] = cm.cm(p); return r
with cf.ThreadPoolExecutor(4) as ex, open(sys.argv[2], 'w') as o:
    for r in ex.map(f, mv): o.write(json.dumps(r) + '\n'); o.flush()
