"""mkvar.py ANFILE NAME: turn the last design line of an anneal2/pfxsearch output into (x2, x1, rx, design.json)"""
import sys, json
l = [x for x in open(sys.argv[1]) if 'X2ORD=' in x][-1].split(' ', 4)
x2 = l[2].split('=')[1]; x1 = l[3].split('=')[1]
d = json.loads(l[4]); f = {int(k): v for k, v in d['f'].items()}
P = {(int(k) if k.lstrip('-').isdigit() else k): v for k, v in d['P'].items()}
rx = []
if P.get('x126_125'): rx.append('126'); P['x126_125'] = (f[126] + 1) // 2
if P.get('x117_130'): rx.append('117')
json.dump({'f': f, 'P': P}, open('des_%s.json' % sys.argv[2], 'w'))
print(x2, x1 or ',', ','.join(rx) or ',')
