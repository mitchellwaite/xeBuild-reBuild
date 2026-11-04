"""fl10k.py: findField's use.  bl as well as sec; signature forms.  Ref has comma's search numbered below nul's in [security] (notes, attempt 10)."""
import fllib as L, fl10lib as F, fl10h as H
S = F.S0
BL = "comma = memFindChar(p, ',', size - pos);\n\t\t\tnul = memFindChar(p, 0, size - pos);\n\t\t\tlen = comma;"
assert S.count(BL) == 1
V = {}
V['bl'] = L.sub(S, BL, "findField(p, size - pos, &comma, &nul);\n\t\t\tlen = comma;")
# raw and flash too, in their order (a second helper would be needed): nul first, via the same helper
RF = "nul = memFindChar(p, 0, size - pos);\n\t\t\tcomma = memFindChar(p, ',', size - pos);"
assert S.count(RF) == 2
V['all4'] = V['bl'].replace(RF, "findField(p, size - pos, &comma, &nul);")
V['raw+flash+sec'] = S.replace(RF, "findField(p, size - pos, &comma, &nul);")
a = S.index("[rawpatch]: name,offset")
b = S.index("[flashfs]: name[,crc]")
V['raw+sec'] = S[:a] + S[a:b].replace(RF, "findField(p, size - pos, &comma, &nul);") + S[b:]
V['flash+sec'] = S[:b] + S[b:].replace(RF, "findField(p, size - pos, &comma, &nul);")
V['bl,raw+sec'] = V['raw+sec'].replace(BL, "findField(p, size - pos, &comma, &nul);\n\t\t\tlen = comma;")
V['bl,flash+sec'] = V['flash+sec'].replace(BL, "findField(p, size - pos, &comma, &nul);\n\t\t\tlen = comma;")
# a nul-first twin for raw/flash
TWIN = "static void findField2(unsigned char *p, int rem, int *comma, int *nul)\n{\n\t*nul = memFindChar(p, 0, rem);\n\t*comma = memFindChar(p, ',', rem);\n}\n\n"
def twin(s):
    return L.sub(s, "/* read the file list ini:", TWIN + "/* read the file list ini:")
V['bl+sec,twin'] = twin(V['bl'].replace(RF, "findField2(p, size - pos, &comma, &nul);"))
V['sec,twin'] = twin(S.replace(RF, "findField2(p, size - pos, &comma, &nul);"))
F.run(V, 'k')
