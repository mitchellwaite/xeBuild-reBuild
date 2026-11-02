"""meas.py INJ.json DESIGN.json [tag]: measure an injection list: inv, L1 to design, order, fq."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import table
inj = [tuple(x) for x in json.load(open(sys.argv[1]))]; des = {int(k): v for k, v in json.load(open(sys.argv[2])).items()}
r = table.meas(inj, sys.argv[3] if len(sys.argv) > 3 else 'm')
fq = r['fq']
print('inv', r['inv'], 'dist', sum(abs(fq.get(b, 0) - v) for b, v in des.items()), 'miss', [b for b in des if b not in fq])
print(r['order']); print({b: (fq.get(b), v) for b, v in des.items() if fq.get(b) != v})
