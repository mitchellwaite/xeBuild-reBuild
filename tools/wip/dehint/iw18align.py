"""helper of iw18align.sh: one tree dump -> the name of the 512-byte memcpy's dest in finalizeImage (ECD loop) with its definition and ptr info line."""
import re, sys
p = sys.argv[1]
t = open(p, errors='replace').read()
m = re.search(r'^;; Function finalizeImage \(.*?(?=^;; Function |\Z)', t, re.S | re.M)
if not m: sys.exit()
b = m.group(0)
out = []
for x in re.finditer(r'(?:__builtin_)?memcpy \(([^,]+), ([^,]+), 512\)', b):
    d = x.group(1)
    if not d.endswith(tuple('0123456789')): continue
    dn = re.escape(d)
    info = re.findall(r'# PT = [^\n]*?\n?[^\n]*?\n?\s*' + dn + r' = [^\n]*', b)
    al = ''
    # the ALIGN line precedes the def, or decl list at the head
    k = re.search(r'([^\n]*)\n\s*(?:# [^\n]*\n\s*)*' + dn + r' = ([^\n]*)', b)
    out.append('%s[%s] %s' % (d, k.group(1).strip()[:90] if k else '?', k.group(2)[:50] if k else ''))
print(p.split('.')[-1], ' | '.join(out))
