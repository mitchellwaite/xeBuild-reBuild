"""try.py JSON-list-of-injections: one measurement (inv incl. missing penalty, order, fq)."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ext, table
inj = [tuple(x) for x in json.loads(sys.argv[1])]
r = table.meas(inj, sys.argv[2] if len(sys.argv) > 2 else 'try')
print(r['inv'], r['needmiss']); print(r['order'])
print({k: r['fq'][k] for k in sorted(r['fq'], key=str)})
