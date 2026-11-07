"""Attempt 48: small natural edits around the SE path and the signature block on attempt 47's
`(int)r < 0` near miss (0 loose / 7 strict: the no-key log copy's .p2align needs the SE copy's
jmp block at frequency 1, i.e. block 110 at 3 or P(<=5) >= 62.5%), every subset.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a48_perturb.py"""
import os, itertools
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src', 'build.c')
NEG = ('if (__builtin_expect(r != 0, 0))\n', 'if ((int)r < 0)\n')
E = {
 'fd': ('setFlashBuild(getBeU16(xb.files[i].data + 2));', 'setFlashBuild(getBeU16(e->data + 2));'),
 'sen': ("if (type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {",
         "if (type == 9)\n\t\t\t\tif (e->data[0] == 'S' && e->data[1] == 'E') {"),
 'st': ('\t\t\t\t\txb.cfLdv = 0;\n\t\t\t\t\txb.seReplacesCf = 1;\n', '\t\t\t\t\txb.seReplacesCf = 1;\n\t\t\t\t\txb.cfLdv = 0;\n'),
 'ty': ('e->type = type = 14;', 'type = 14;\n\t\t\t\t\te->type = type;'),
 'ck': ('\t\t\t\tr = checkBl(e->data, e->size, type, e->crc);\n\t\t\t\tif (r)\n',
        '\t\t\t\tr = checkBl(e->data, e->size, type, e->crc);\n\t\t\t\tif ((int)r < 0)\n'),
 'et': ('\t\t\t\tif (type == 14)\n\t\t\t\t\tsetFlashBuild', '\t\t\t\tif (e->type == 14)\n\t\t\t\t\tsetFlashBuild'),
 'lt': ('if (xb.type <= BUILD_DEVGL16) {\n\t\t\t\t\tif ((int)r', 'if (xb.type < BUILD_DEVKIT) {\n\t\t\t\t\tif ((int)r'),
}
V = {}
keys = list(E)
for n in range(0, 4):
    for c in itertools.combinations(keys, n):
        V['n_' + ('_'.join(c) or 'base')] = [NEG] + [E[k] for k in c]
