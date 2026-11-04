"""fl4e.py: loop forms of setupFiles with the test first in block order (so xb.nFiles gets a lower number than i when inlined)."""
import fllib as L, fl4lib as F
import fl4d as D
B = D.BASE
FOR = D.FOR
FORMS = {
 'forbreak': '\tfor (i = 0; ; i++) {\n\t\tif (i >= xb.nFiles)\n\t\t\tbreak;\n\t\te = &xb.files[i];\n',
 'forbreak2': '\tfor (i = 0; ; i++) {\n\t\tif (xb.nFiles <= i)\n\t\t\tbreak;\n\t\te = &xb.files[i];\n',
}
V = {'': B}
for k, v in FORMS.items():
    V[k] = L.sub(B, FOR, v)
    V[k + '+ret'] = L.sub(B, FOR, v.replace('break', 'return'))
F.run(V, 'e')
