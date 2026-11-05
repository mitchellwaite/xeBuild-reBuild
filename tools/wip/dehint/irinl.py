"""python tools/wip/dehint/irinl.py <file.c> <pattern> [ctx] : grep the ipa-inline details dump of <file.c> for
<pattern>, `ctx` lines after each match."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib

path, pat = sys.argv[1:3]
ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 3
text = open(path, newline='').read().replace('\r\n', '\n')
ok, o, d = irlib.compile_src(text, ['-fdump-ipa-inline-details'])
if not ok:
    print(o)
    sys.exit(1)
for name in os.listdir(d):
    if name.endswith('inline') or '-inline' in name or re.search(r'i\.inline$', name):
        ls = open(os.path.join(d, name), errors='replace').read().split('\n')
        i = 0
        while i < len(ls):
            if re.search(pat, ls[i]):
                print('\n'.join(ls[i:i + ctx + 1]))
                print('--')
                i += ctx
            i += 1
irlib.cleanup(d)
