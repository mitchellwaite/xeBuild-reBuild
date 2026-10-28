import os, sys, json
# usage: env as fake7; python dbg.py file.out key=val ...   (f:B=v / P:B=v)
sys.argv, args = ['x', '0', '1'], sys.argv[1:]
import fake7, fibsim
l = [x for x in open(args[0]) if x.startswith('best')][0]
d = json.loads(l.split(' ', 2)[2])
f = {int(k): v for k, v in d['f'].items()}
P = {(int(k) if k.lstrip('-').isdigit() else k): v for k, v in d['P'].items()}
for a in args[1:]:
    k, v = a.split('='); kind, b = k.split(':'); b = int(b) if b.lstrip('-').isdigit() else b
    (f if kind == 'f' else P)[b] = int(v)
PP = dict(P); print('ok', fake7.ok(f, PP))
# instrument extract_min
orig = fibsim.Heap.extract_min
log = []
def em(self):
    z = orig(self); log.append((z.data, z.key)); return z
fibsim.Heap.extract_min = em
o = fake7.sim(f, PP)
print('inv', fake7.inv(o))
i = max(i for i, (b, k) in enumerate(log) if b == 94)
print(' '.join('%s:%d' % (b, -k if k > -1000000 else -k - 1000000) for b, k in log[i:] if b in fake7.mcsim2.pos or b == 94))
