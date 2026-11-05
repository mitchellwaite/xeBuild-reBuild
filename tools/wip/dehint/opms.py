"""opms.py file.c [fn]: multiset difference of fn's instructions (default _applyIniOptions)
against the reference, jump/call targets dropped: empty means only the layout differs."""
import collections, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

fn = sys.argv[2] if len(sys.argv) > 2 else '_applyIniOptions'
ok, o, d = optlib.compile_src(optlib.read_src(sys.argv[1]))
if not ok:
    print(o); sys.exit(1)
fns, _ = optlib.disasm(o)
J = re.compile(r'^(j\w+|call)\s+[0-9a-f]+$')
nop = re.compile(r'^(nop|xchg\s+ax,ax|lea\s+esi,\[esi.*\]|lea\s+edi,\[edi.*\]|mov\s+esi,esi|mov\s+edi,edi)')


def ms(ls):
    out = collections.Counter()
    for l in optlib.norm(ls):
        l = l.strip()
        if nop.match(l):
            continue
        out[J.sub(r'\1', l)] += 1
    return out


a = ms(optlib._ref['fns'][fn]); b = ms(fns[fn])
print('ref', sum(a.values()), 'ours', sum(b.values()))
for k, v in sorted((a - b).items()):
    print('-', v, k)
for k, v in sorted((b - a).items()):
    print('+', v, k)
optlib.cleanup(d)
