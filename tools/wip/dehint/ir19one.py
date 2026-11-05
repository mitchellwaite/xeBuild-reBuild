"""Attempt 19: python tools/wip/dehint/ir19one.py <module> <function-call-expression> [pass,...]: score one generator form, loose diff, dumps of the named passes (body only)."""
import importlib, re, sys
sys.path.insert(0, __file__.rsplit('\\', 1)[0].rsplit('/', 1)[0])
from ir17lib import put, score, diff
from ir19cfg import analyse

m = importlib.import_module(sys.argv[1])
f = eval(sys.argv[2], vars(m))
t = put(f)
print(score(t))
print(diff(t))
if len(sys.argv) > 3:
    a = analyse(t)
    print({k: v for k, v in a[0].items() if k != '_passes'})
    for p in sys.argv[3].split(','):
        print('=====', p)
        b = a[1].get(p, '')
        i = b.find('<bb 2>')
        print('\n'.join(l[:105] for l in b[i:].split('\n') if l.strip() and not re.match(r'\s*(\.MEM|#\s*\.MEM|#\s*VUSE)', l)))
