"""srcx.py: extends s19 search with chain sources: 's<t>' = an `if (bcp) goto` placed right
before call statement t (post-loop mode_client targets), allowed only to later targets t2 > t."""
import os, sys
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(ROOT, 'tools', 'wip', 'mc', 's19'))
import search
POST = [t for t, (k, off) in enumerate(search.TGT) if k == 'mc' and off > search.LOOP1]
for t in POST:
    search.SRCS['s%d' % t] = (search.TGT[t][1], os.environ.get('CVAR', 'arg'), 'chain')
_ok = search.ok
def ok(t, s):
    if s.startswith('s') and s[1:].isdigit():
        return t in POST and t > int(s[1:])
    return _ok(t, s)
search.ok = ok
