"""keysshow.py <fn> <file|-> [site,site..]: side-by-side of fn against the reference.

file '-' means src/keys.c; sites are names from keyssubset.SITES (prefix fc:/kv:/dae:).
Flags come from KEYSFLAGS (space separated) if set."""
import difflib, os, sys
import keyslib as K
import keyssubset as S

fn, f = sys.argv[1], sys.argv[2]
s = K.base() if f == '-' else open(f, newline='').read()
if len(sys.argv) > 3 and sys.argv[3]:
    for x in sys.argv[3].split(','):
        w, n = x.split(':')
        for name, old, new in S.SITES[w]:
            if name == n:
                assert old in s, old
                s = s.replace(old, new)
fl = os.environ.get('KEYSFLAGS')
o = K.compile(s, fl.split() if fl else None, 'show')
print('MATCH' if K.same(o) else 'differ', K.fndiff(o))
a = K.dis(K.REF)[fn]
b = K.dis(o)[fn]
if os.environ.get('RAW'):
    print('\n'.join(a))
    sys.exit()
for ln in difflib.unified_diff(a, b, 'ref', 'new', lineterm='', n=int(os.environ.get('CTX', 2))):
    print(ln)
