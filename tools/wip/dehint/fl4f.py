"""fl4f.py: base for what follows: setupFiles with its test first."""
import fllib as L, fl4lib as F, fl4d as D
FORM = '\tfor (i = 0; ; i++) {\n\t\tif (i >= xb.nFiles)\n\t\t\tbreak;\n\t\te = &xb.files[i];\n'
BASE = L.sub(D.BASE, D.FOR, FORM)
if __name__ == '__main__':
    import os
    open(os.path.join(F.A4, 'f.c'), 'w', newline='\n').write(BASE)
