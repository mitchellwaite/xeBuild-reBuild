# gk.py BASE OUT SPEC... : SPEC = off:form, off = line offset from the arg-loop 'for', form A=(c)&&!k  B=!k&&(c)  C=k||(c)
import sys, re, os
KV = os.environ.get('KV', 'k')
s = open(sys.argv[1]).read().split('\n')
f = ([i for i, x in enumerate(s) if 'for (i = 0; i < argc; i++) {' in x] + [0])[0]
if not any('int %s = __builtin_constant_p' % KV in x for x in s):
    j = [i for i, x in enumerate(s) if 'log_set_name("client");' in x][0]
    s.insert(j + 1, '\tint %s = __builtin_constant_p(argc);' % KV); f += 1
for sp in sys.argv[3:]:
    o, fm = sp.split(':'); L = f + int(o); x = s[L]
    m = re.match(r'^(\s*(?:\} else )?if )\((.*)\)(\s*\{?)$', x)
    assert m, (o, x)
    c = m.group(2)
    n = {'A': '((%s) && !KV)', 'B': '(!KV && (%s))', 'C': '(KV || (%s))'}[fm].replace('KV', KV) % c
    s[L] = m.group(1) + n + m.group(3)
open(sys.argv[2], 'w', newline='\n').write('\n'.join(s))
