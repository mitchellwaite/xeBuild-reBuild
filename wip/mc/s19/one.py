"""one.py '<json injections>': write build/v/mc19/v_one.c and print mckeys for it"""
import json, os, subprocess, sys
sys.argv += []
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import search as S
inj = [tuple(x) for x in json.loads(sys.argv[1])]
p = os.path.join(S.D, 'v_one.c')
open(p, 'w', newline='\n').write(S.make(inj))
r = subprocess.run([sys.executable, os.path.join(S.ROOT, 'wip', 'mc', 'mckeys.py'), p] + S.FLAGS, capture_output=True, text=True)
print(r.stdout[-3000:], r.stderr[-500:])
