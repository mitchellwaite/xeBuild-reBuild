"""fl9l.py: write the draft (d) and its no-findField form (n) as a9/d.c, a9/n.c for fl9h.py, fl9c.py"""
import os
os.environ.setdefault('FLA', 'a9')
import fllib as L, fl6lib as F, fl9final

d = fl9final.source()
open(os.path.join(L.BD, 'a9', 'd.c'), 'w', newline='\n').write(d)
n = L.sub(d, fl9final.NEWFFC + "static void findField(unsigned char *p, int rem, int *comma, int *nul)\n{\n\t*comma = memFindChar(p, ',', rem);\n\t*nul = memFindChar(p, 0, rem);\n}\n\n", '')
n = F.secsub(n, 'sec', F.CALL, F.CFIRST)
open(os.path.join(L.BD, 'a9', 'n.c'), 'w', newline='\n').write(n)
