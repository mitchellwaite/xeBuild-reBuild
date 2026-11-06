# mode_client attempt 3: attempt 2's -i/-p pin variants (mc2v_ip, mc2v_ip2) respelled for the
# `arg = argv[i + 1]; i++;` base, plus the same rewrite applied to the variants' new text.
import os, re, runpy
D = os.path.dirname(os.path.abspath(__file__))


def fix(s):
    return re.sub(r'(\t*)(\w+) = argv\[\+\+i\];', lambda m: '%s%s = argv[i + 1];\n%si++;' % (m.group(1), m.group(2), m.group(1)), s)


V = {}
for f in ('mc2v_ip.py', 'mc2v_ip2.py'):
    for k, subs in runpy.run_path(os.path.join(D, f))['V'].items():
        V[f[5:-3] + ':' + k] = [(fix(o), fix(n)) for o, n in subs]
