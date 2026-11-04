"""fl6s.py: live split tests in parseIni (ifcombine merges them, at pass 103, before dom2/dom3 pop free names): the loop ends and others,
at the subsets of parseIni's three dead tests.  Also the short-circuit and else forms of findKey's split."""
import itertools, sys
import fllib as L, fl6lib as F

SP = {
    'rawE': ('raw', "\t\t\tif (pos >= end)\n\t\t\t\ti = 16;\n", ["\t\t\tif (pos > end)\n\t\t\t\ti = 16;\n\t\t\tif (pos == end)\n\t\t\t\ti = 16;\n",
                                                               "\t\t\tif (pos == end)\n\t\t\t\ti = 16;\n\t\t\tif (pos > end)\n\t\t\t\ti = 16;\n"]),
    'flE': ('flash', "\t\t\tif (pos >= size)\n\t\t\t\ti = 256;\n", ["\t\t\tif (pos > size)\n\t\t\t\ti = 256;\n\t\t\tif (pos == size)\n\t\t\t\ti = 256;\n",
                                                                  "\t\t\tif (pos == size)\n\t\t\t\ti = 256;\n\t\t\tif (pos > size)\n\t\t\t\ti = 256;\n"]),
    'secE': ('sec', "\t\t\tif (pos >= end)\n\t\t\t\ti = 10;\n", ["\t\t\tif (pos > end)\n\t\t\t\ti = 10;\n\t\t\tif (pos == end)\n\t\t\t\ti = 10;\n",
                                                               "\t\t\tif (pos == end)\n\t\t\t\ti = 10;\n\t\t\tif (pos > end)\n\t\t\t\ti = 10;\n"]),
    'flC': ('flash', "\t\t\tif (comma >= 0 && comma < nul) {\n", ["\t\t\tif (comma >= 0) {\n\t\t\t\tif (comma < nul) {\n\t\t\t\t\tlen = comma;\n\t\t\t\t\tnoCrc = 0;\n\t\t\t\t}\n\t\t\t}\n\t\t\tif (0) {\n"]),
    'flD': ('flash', "\t\t\t\tif (xb.firmware[i][len - 1] == '1' || xb.firmware[i][len - 1] == '2')\n\t\t\t\t\txb.firmware[i][len - 1] = 0;\n",
            ["\t\t\t\tif (xb.firmware[i][len - 1] == '1')\n\t\t\t\t\txb.firmware[i][len - 1] = 0;\n\t\t\t\tif (xb.firmware[i][len - 1] == '2')\n\t\t\t\t\txb.firmware[i][len - 1] = 0;\n"]),
    'blE': ('bl', "\t\t\tif (pos > end) {\n", ["\t\t\tif (pos >= end + 1) {\n"]),
}
DR = ['T1,T3', 'T1,T2,T3', 'T2,T3', 'T1,T2', 'T1', 'T2', 'T3', '']
V = {}
keys = list(SP)
for d in DR:
    base = F.drop(F.S0, [x for x in d.split(',') if x])
    for r in (1, 2, 3):
        for sub in itertools.combinations(keys, r):
            for forms in itertools.product(*[range(len(SP[k][2])) for k in sub]):
                s = base
                for k, f in zip(sub, forms):
                    s = F.secsub(s, SP[k][0], SP[k][1], SP[k][2][f])
                V['%s|%s' % (d, '+'.join('%s%d' % (k, f) for k, f in zip(sub, forms)))] = s
print(len(V))
if __name__ == '__main__':
    F.run(V, 's', 25)
