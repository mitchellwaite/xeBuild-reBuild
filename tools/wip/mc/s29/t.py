"""t.py TAG 'SPECJSON' : gen + measure (+fncmp)."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen, m
import specs
spec = eval(sys.argv[2], vars(specs))
if 'J' in spec and isinstance(spec['J'], dict): spec['J'] = {int(k): v for k, v in spec['J'].items()}
r = m.meas(gen.make(spec), sys.argv[1], fncmp=True)
for k in ('err', 'inv', 'miss', 'fncmp', 'order'):
    if k in r: print(k, r[k])
if 'raw' in r: print(r['raw'][3])
