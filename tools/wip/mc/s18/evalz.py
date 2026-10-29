import sys, json, os
src = sys.argv[1]; sys.argv = ['x', '0', '1']
import fake7
l = open(src).read().split(' ', 4)
fake7.X2ORD = [int(x) for x in l[2].split('=')[1].split(',') if x]
fake7.X1ORD = [int(x) for x in l[3].split('=')[1].split(',') if x]
d = json.loads(l[4]); f = {int(k): v for k, v in d['f'].items()}
P = {(int(k) if k.lstrip('-').isdigit() else k): v for k, v in d['P'].items()}
if P.get('x126_125'): P['x126_125'] = (f[126] + 1) // 2
PP = dict(P); print('ok', fake7.ok(f, PP)); o = fake7.sim(f, PP); print('inv', fake7.inv(o)); print(' '.join(map(str, o)))
print('X2ORD', fake7.X2ORD, 'X1ORD', fake7.X1ORD); print(json.dumps({'f': f, 'P': P}))
