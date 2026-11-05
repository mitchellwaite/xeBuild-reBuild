"""python tools/wip/dehint/irbb.py <file.c> <fn> [passsuffix ...]: compile with -fdump-tree-all-blocks-details and rtl-bbro/expand,
print for each named tree pass (default profile_estimate/042, dom2-ish optimized) every block of <fn>: bb, freq, succ[%], first call string."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib

src, fn = sys.argv[1:3]
want = sys.argv[3:] or ['profile_estimate', 'optimized']
text = open(src, newline='').read().replace('\r\n', '\n')
ok, o, d = irlib.compile_src(text, [], extra=['-fdump-tree-profile_estimate-blocks-details', '-fdump-tree-optimized-blocks-details', '-fdump-tree-dom2-blocks-details', '-fdump-tree-dom3-blocks-details', '-fdump-tree-vrp1-blocks-details'])
if not ok:
    print(o)
    sys.exit(1)
for w in want:
    fs = [x for x in os.listdir(d) if x.endswith(w)]
    if not fs:
        print('no dump', w, os.listdir(d)[:10])
        continue
    t = open(os.path.join(d, fs[0]), errors='replace').read()
    i = t.find(';; Function %s ' % fn)
    t = t[i:]
    j = t.find('\n;; Function ', 10)
    if j > 0:
        t = t[:j]
    # keep only the final CFG: the last 'fn (...)' body
    k = t.rfind('\n%s (' % fn)
    t = t[k:]
    print('==', w)
    for b in re.split(r'(?m)^;;   basic block ', t)[1:]:
        m = re.match(r'(\d+), loop depth (\d+), count \d+, freq (\d+)', b)
        succ = re.search(r'succ:(.*?)(?:\n\s*\n|\n[^;\n]*[<\w_]+ *[(=]|$)', b, re.S)
        ss = re.findall(r'(?:succ:)?\s+(\d+|EXIT)\s*\[([\d.]+)%\]', b[b.find('succ:'):]) if 'succ:' in b else []
        calls = re.findall(r'(\w+) \(.*?"([^"]{0,28})', b)
        cond = re.findall(r'if \((.*?)\)', b)
        print('bb%-3s f=%-6s -> %-32s %s %s' % (m.group(1), m.group(3), ' '.join('%s[%s]' % x for x in ss), ('if(' + cond[0] + ')') if cond else '', ' '.join(c[1][:24] for c in calls)))
irlib.cleanup(d)
