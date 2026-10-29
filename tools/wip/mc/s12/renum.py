"""renum.py BBRO OUT [XBB]: mode_client section with the asm-goto block XBB -> 999 and later bbs -1 (sp numbering)"""
import re, sys
t = open(sys.argv[1]).read()
i = t.index(';; Function mode_client'); j = t.find('\n;; Function ', i + 10); t = t[i:j if j > 0 else None]
X = int(sys.argv[3]) if len(sys.argv) > 3 else 105
def f(m):
    n = int(m.group(2))
    n = 999 if n == X else (n - 1 if n > X else n)
    return m.group(1) + str(n)
open(sys.argv[2], 'w').write(re.sub(r'((?:bb |block |round: |Block |for bb ))(\d+)', f, t))
